"""
Command-line interface for TTS Agents.

This module provides a comprehensive CLI for the TTS Agents library
with rich output, progress tracking, and multiple operation modes.
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Optional, List
import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint

from .core import TTSAgent
from .batch import BatchProcessor
from .streaming import StreamingTTS
from .models import TTSRequest, Voice, AudioFormat, TTSModel, TTSConfig
from .exceptions import TTSAgentError


# Initialize rich console
console = Console()


@click.group()
@click.option('--api-key', envvar='OPENAI_API_KEY', help='OpenAI API key')
@click.option('--base-url', help='OpenAI API base URL')
@click.option('--timeout', default=30, help='Request timeout in seconds')
@click.option('--max-retries', default=3, help='Maximum retry attempts')
@click.option('--rate-limit-delay', default=1.0, help='Delay between requests')
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose logging')
@click.pass_context
def cli(ctx, api_key, base_url, timeout, max_retries, rate_limit_delay, verbose):
    """TTS Agents - Professional Text-to-Speech with OpenAI TTS-1"""
    
    # Setup logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create TTS config
    config = TTSConfig(
        api_key=api_key,
        base_url=base_url,
        timeout=timeout,
        max_retries=max_retries,
        rate_limit_delay=rate_limit_delay
    )
    
    # Store config in context
    ctx.ensure_object(dict)
    ctx.obj['config'] = config


@cli.command()
@click.argument('text')
@click.option('--voice', '-v', type=click.Choice([v.value for v in Voice]), default='alloy', help='Voice to use')
@click.option('--model', '-m', type=click.Choice([m.value for m in TTSModel]), default='tts-1', help='TTS model to use')
@click.option('--format', '-f', type=click.Choice([f.value for f in AudioFormat]), default='mp3', help='Audio format')
@click.option('--speed', '-s', type=float, default=1.0, help='Speech speed (0.25-4.0)')
@click.option('--output', '-o', default='output.mp3', help='Output file path')
@click.option('--streaming', is_flag=True, help='Use streaming for better performance')
@click.pass_context
def generate(ctx, text, voice, model, format, speed, output, streaming):
    """Generate speech from text"""
    
    async def _generate():
        config = ctx.obj['config']
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Generating speech...", total=None)
            
            try:
                async with TTSAgent(config) as agent:
                    if streaming:
                        # Use streaming TTS
                        streaming_tts = StreamingTTS(agent)
                        response = await streaming_tts.stream_speech_to_file(
                            text=text,
                            output_path=output,
                            voice=Voice(voice),
                            model=TTSModel(model),
                            format=AudioFormat(format),
                            speed=speed
                        )
                    else:
                        # Use regular TTS
                        response = await agent.generate_speech(
                            text=text,
                            voice=Voice(voice),
                            model=TTSModel(model),
                            format=AudioFormat(format),
                            speed=speed,
                            output_path=output
                        )
                    
                    if response.success:
                        progress.update(task, description="✅ Speech generated successfully!")
                        
                        # Display results
                        table = Table(title="Generation Results")
                        table.add_column("Property", style="cyan")
                        table.add_column("Value", style="green")
                        
                        table.add_row("Text", text[:50] + "..." if len(text) > 50 else text)
                        table.add_row("Voice", voice)
                        table.add_row("Model", model)
                        table.add_row("Format", format)
                        table.add_row("Speed", str(speed))
                        table.add_row("Output File", str(response.file_path or output))
                        table.add_row("File Size", f"{response.file_size} bytes" if response.file_size else "N/A")
                        
                        console.print(table)
                    else:
                        console.print(f"[red]❌ Generation failed: {response.error}[/red]")
                        sys.exit(1)
            
            except TTSAgentError as e:
                console.print(f"[red]❌ TTS Agent Error: {str(e)}[/red]")
                sys.exit(1)
            except Exception as e:
                console.print(f"[red]❌ Unexpected Error: {str(e)}[/red]")
                sys.exit(1)
    
    asyncio.run(_generate())


@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.option('--voice', '-v', type=click.Choice([v.value for v in Voice]), default='alloy', help='Voice to use')
@click.option('--model', '-m', type=click.Choice([m.value for m in TTSModel]), default='tts-1', help='TTS model to use')
@click.option('--format', '-f', type=click.Choice([f.value for f in AudioFormat]), default='mp3', help='Audio format')
@click.option('--speed', '-s', type=float, default=1.0, help='Speech speed (0.25-4.0)')
@click.option('--output', '-o', default='output.mp3', help='Output file path')
@click.option('--streaming', is_flag=True, help='Use streaming for better performance')
@click.pass_context
def file(ctx, input_file, voice, model, format, speed, output, streaming):
    """Generate speech from text file"""
    
    async def _file():
        config = ctx.obj['config']
        
        try:
            # Read input file
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read().strip()
            
            if not text:
                console.print("[red]❌ Input file is empty[/red]")
                sys.exit(1)
            
            console.print(f"[green]📖 Read {len(text)} characters from {input_file}[/green]")
            
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Generating speech from file...", total=None)
                
                try:
                    async with TTSAgent(config) as agent:
                        if streaming:
                            # Use streaming TTS
                            streaming_tts = StreamingTTS(agent)
                            response = await streaming_tts.stream_speech_to_file(
                                text=text,
                                output_path=output,
                                voice=Voice(voice),
                                model=TTSModel(model),
                                format=AudioFormat(format),
                                speed=speed
                            )
                        else:
                            # Use regular TTS
                            response = await agent.generate_speech(
                                text=text,
                                voice=Voice(voice),
                                model=TTSModel(model),
                                format=AudioFormat(format),
                                speed=speed,
                                output_path=output
                            )
                        
                        if response.success:
                            progress.update(task, description="✅ Speech generated successfully!")
                            
                            # Display results
                            table = Table(title="File Generation Results")
                            table.add_column("Property", style="cyan")
                            table.add_column("Value", style="green")
                            
                            table.add_row("Input File", input_file)
                            table.add_row("Text Length", str(len(text)))
                            table.add_row("Voice", voice)
                            table.add_row("Model", model)
                            table.add_row("Format", format)
                            table.add_row("Speed", str(speed))
                            table.add_row("Output File", str(response.file_path or output))
                            table.add_row("File Size", f"{response.file_size} bytes" if response.file_size else "N/A")
                            
                            console.print(table)
                        else:
                            console.print(f"[red]❌ Generation failed: {response.error}[/red]")
                            sys.exit(1)
                
                except TTSAgentError as e:
                    console.print(f"[red]❌ TTS Agent Error: {str(e)}[/red]")
                    sys.exit(1)
                except Exception as e:
                    console.print(f"[red]❌ Unexpected Error: {str(e)}[/red]")
                    sys.exit(1)
        
        except FileNotFoundError:
            console.print(f"[red]❌ File not found: {input_file}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]❌ Error reading file: {str(e)}[/red]")
            sys.exit(1)
    
    asyncio.run(_file())


@cli.command()
@click.argument('texts', nargs=-1)
@click.option('--input-file', '-f', type=click.Path(exists=True), help='File containing texts (one per line)')
@click.option('--voice', '-v', type=click.Choice([v.value for v in Voice]), default='alloy', help='Voice to use')
@click.option('--model', '-m', type=click.Choice([m.value for m in TTSModel]), default='tts-1', help='TTS model to use')
@click.option('--format', '-f', type=click.Choice([f.value for f in AudioFormat]), default='mp3', help='Audio format')
@click.option('--speed', '-s', type=float, default=1.0, help='Speech speed (0.25-4.0)')
@click.option('--output-dir', '-o', default='./output', help='Output directory for audio files')
@click.option('--concurrent', '-c', default=5, help='Maximum concurrent requests')
@click.option('--retry-attempts', default=3, help='Number of retry attempts')
@click.pass_context
def batch(ctx, texts, input_file, voice, model, format, speed, output_dir, concurrent, retry_attempts):
    """Process multiple texts in batch"""
    
    async def _batch():
        config = ctx.obj['config']
        
        # Collect texts
        all_texts = list(texts)
        
        if input_file:
            try:
                with open(input_file, 'r', encoding='utf-8') as f:
                    file_texts = [line.strip() for line in f if line.strip()]
                all_texts.extend(file_texts)
            except Exception as e:
                console.print(f"[red]❌ Error reading input file: {str(e)}[/red]")
                sys.exit(1)
        
        if not all_texts:
            console.print("[red]❌ No texts provided[/red]")
            sys.exit(1)
        
        console.print(f"[green]📝 Processing {len(all_texts)} texts in batch[/green]")
        
        # Create batch requests
        requests = [
            TTSRequest(
                text=text,
                voice=Voice(voice),
                model=TTSModel(model),
                format=AudioFormat(format),
                speed=speed
            )
            for text in all_texts
        ]
        
        try:
            async with TTSAgent(config) as agent:
                batch_processor = BatchProcessor(agent, max_concurrent=concurrent)
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    BarColumn(),
                    TaskProgressColumn(),
                    console=console
                ) as progress:
                    task = progress.add_task("Processing batch...", total=len(requests))
                    
                    # Process batch
                    result = await batch_processor.process_batch(
                        requests=requests,
                        output_directory=output_dir,
                        retry_attempts=retry_attempts
                    )
                    
                    progress.update(task, completed=len(requests), description="✅ Batch processing completed!")
                    
                    # Display results
                    table = Table(title="Batch Processing Results")
                    table.add_column("Metric", style="cyan")
                    table.add_column("Value", style="green")
                    
                    table.add_row("Total Requests", str(result.total_requests))
                    table.add_row("Successful", str(result.successful))
                    table.add_row("Failed", str(result.failed))
                    table.add_row("Processing Time", f"{result.processing_time:.2f}s")
                    table.add_row("Output Directory", output_dir)
                    
                    console.print(table)
                    
                    if result.errors:
                        console.print("\n[red]❌ Errors:[/red]")
                        for error in result.errors:
                            console.print(f"  • {error}")
        
        except TTSAgentError as e:
            console.print(f"[red]❌ TTS Agent Error: {str(e)}[/red]")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]❌ Unexpected Error: {str(e)}[/red]")
            sys.exit(1)
    
    asyncio.run(_batch())


@cli.command()
def voices():
    """List available voices"""
    
    table = Table(title="Available Voices")
    table.add_column("Voice", style="cyan")
    table.add_column("Description", style="green")
    
    voice_descriptions = {
        "alloy": "Neutral, balanced voice",
        "echo": "Clear, articulate voice",
        "fable": "Warm, storytelling voice",
        "onyx": "Deep, authoritative voice",
        "nova": "Bright, energetic voice",
        "shimmer": "Soft, gentle voice"
    }
    
    for voice in Voice:
        description = voice_descriptions.get(voice.value, "Professional voice")
        table.add_row(voice.value, description)
    
    console.print(table)


@cli.command()
def models():
    """List available models"""
    
    table = Table(title="Available Models")
    table.add_column("Model", style="cyan")
    table.add_column("Description", style="green")
    
    model_descriptions = {
        "tts-1": "Standard quality, faster processing",
        "tts-1-hd": "High quality, slower processing"
    }
    
    for model in TTSModel:
        description = model_descriptions.get(model.value, "TTS model")
        table.add_row(model.value, description)
    
    console.print(table)


@cli.command()
def formats():
    """List available audio formats"""
    
    table = Table(title="Available Audio Formats")
    table.add_column("Format", style="cyan")
    table.add_column("Description", style="green")
    
    format_descriptions = {
        "mp3": "MP3 audio format (recommended)",
        "opus": "Opus audio format",
        "aac": "AAC audio format",
        "flac": "FLAC lossless format"
    }
    
    for format in AudioFormat:
        description = format_descriptions.get(format.value, "Audio format")
        table.add_row(format.value, description)
    
    console.print(table)


def main():
    """Main CLI entry point."""
    try:
        cli()
    except KeyboardInterrupt:
        console.print("\n[yellow]⚠️  Operation cancelled by user[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected error: {str(e)}[/red]")
        sys.exit(1)


if __name__ == '__main__':
    main()
