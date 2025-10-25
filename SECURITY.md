# Security Policy

## Supported Versions

We actively support the following versions of TTS Agents:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

We take security seriously. If you discover a security vulnerability in TTS Agents, please follow these steps:

### 1. **DO NOT** create a public GitHub issue

Security vulnerabilities should be reported privately to avoid potential exploitation.

### 2. Email us directly

Send an email to: **muhammadbilalkhan@ai.com**

Include the following information:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact assessment
- Any suggested fixes or mitigations
- Your contact information (optional)

### 3. Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Resolution**: Within 30 days (depending on complexity)

### 4. Responsible Disclosure

We follow responsible disclosure practices:
- We will acknowledge receipt of your report
- We will keep you informed of our progress
- We will credit you in our security advisories (unless you prefer to remain anonymous)
- We will not take legal action against security researchers who follow these guidelines

## Security Best Practices

### For Users

1. **Keep Dependencies Updated**
   ```bash
   pip install --upgrade tts-agents
   ```

2. **Use Environment Variables for API Keys**
   ```bash
   export OPENAI_API_KEY="your-secure-api-key"
   ```

3. **Validate Input Data**
   ```python
   # Always validate text input
   if not text or len(text.strip()) == 0:
       raise ValueError("Text cannot be empty")
   ```

4. **Use HTTPS for API Calls**
   ```python
   config = TTSConfig(
       base_url="https://api.openai.com/v1"  # Always use HTTPS
   )
   ```

5. **Implement Rate Limiting**
   ```python
   config = TTSConfig(
       rate_limit_delay=1.0,  # Add delay between requests
       max_retries=3
   )
   ```

### For Developers

1. **Code Security**
   - Use type hints and validation
   - Implement proper error handling
   - Follow secure coding practices
   - Regular security audits

2. **Dependency Management**
   - Keep dependencies updated
   - Use security scanning tools
   - Monitor for vulnerabilities

3. **Testing**
   - Include security tests
   - Test error conditions
   - Validate input sanitization

## Security Features

### Built-in Security Measures

1. **Input Validation**
   - Text length limits
   - Character encoding validation
   - Speed and format validation

2. **Error Handling**
   - Secure error messages
   - No sensitive data in logs
   - Graceful failure handling

3. **Rate Limiting**
   - Configurable request delays
   - Concurrent request limits
   - Automatic retry with backoff

4. **API Security**
   - Secure API key handling
   - HTTPS enforcement
   - Request timeout protection

### Security Configuration

```python
from tts_agents import TTSConfig

# Secure configuration
config = TTSConfig(
    api_key="your-secure-api-key",
    base_url="https://api.openai.com/v1",  # HTTPS only
    timeout=30,  # Request timeout
    max_retries=3,  # Limit retries
    rate_limit_delay=1.0,  # Rate limiting
)

# Enable security features
config.enable_security_checks = True
config.enable_rate_limiting = True
```

## Known Security Considerations

### 1. API Key Security
- **Risk**: API keys exposed in logs or code
- **Mitigation**: Use environment variables, never commit keys to version control

### 2. Input Validation
- **Risk**: Malicious input causing API errors
- **Mitigation**: Comprehensive input validation and sanitization

### 3. Rate Limiting
- **Risk**: API abuse and excessive costs
- **Mitigation**: Built-in rate limiting and request throttling

### 4. Error Information Disclosure
- **Risk**: Sensitive information in error messages
- **Mitigation**: Sanitized error messages, no internal details exposed

## Security Updates

We regularly update TTS Agents to address security issues:

- **Critical**: Immediate patch release
- **High**: Patch within 7 days
- **Medium**: Patch within 30 days
- **Low**: Patch in next minor release

## Security Tools

### Recommended Security Tools

1. **Dependency Scanning**
   ```bash
   pip install safety
   safety check
   ```

2. **Code Security Analysis**
   ```bash
   pip install bandit
   bandit -r src/
   ```

3. **Vulnerability Scanning**
   ```bash
   pip install pip-audit
   pip-audit
   ```

### CI/CD Security

Our CI/CD pipeline includes:
- Automated security scanning
- Dependency vulnerability checks
- Code quality analysis
- Security-focused testing

## Security Contacts

- **Primary**: muhammadbilalkhan@ai.com
- **GitHub**: [@muhammadbilalkhan](https://github.com/muhammadbilalkhan)
- **LinkedIn**: [Muhammad Bilal Khan](https://linkedin.com/in/muhammadbilalkhan)

## Security Acknowledgments

We thank the following security researchers for their contributions:

- [Your name here] - [Vulnerability description]
- [Your name here] - [Vulnerability description]

## Security Changelog

### Version 1.0.0
- Initial security implementation
- Comprehensive input validation
- Secure error handling
- Rate limiting protection
- API key security measures

---

**Last Updated**: October 26, 2024
**Next Review**: January 26, 2025
