# Security Guidelines for IntelliFlow

## Overview
This document outlines the security measures implemented in IntelliFlow and best practices for secure deployment.

## Security Vulnerabilities Fixed

### 1. **Hardcoded API Keys** - CRITICAL
- **Issue**: API keys were hardcoded in source files
- **Fix**: Moved all API keys to environment variables with `.env` file support
- **Files affected**: `ariel_view/backend/app.py`, test files

### 2. **Unsafe Code Execution** - HIGH
- **Issue**: Use of `eval()` function for parsing LLM responses
- **Fix**: Replaced with safe JSON parsing with fallback
- **File**: `ariel_view/tools/enhanced_youtube_tool.py`

### 3. **Overly Permissive CORS** - MEDIUM
- **Issue**: CORS allowed all origins (`*`)
- **Fix**: Restricted to specific localhost origins for development
- **File**: `ariel_view/backend/app.py`

### 4. **Code Injection via `exec()`** - HIGH
- **Issue**: Dynamic code execution in CodeEngine tool
- **Mitigation**: This is intentional functionality but requires secure deployment
- **File**: `agentpro/tools/code_tool.py`

## Security Best Practices

### Environment Variables
1. **Never commit `.env` files** - Use `.env.example` as template
2. **Use strong, unique API keys** for each service
3. **Rotate API keys regularly**
4. **Validate all environment variables** at startup

### API Security
1. **Rate limiting** - Implement on production deployments
2. **Input validation** - Sanitize all user inputs
3. **HTTPS only** - Never deploy without SSL/TLS
4. **Authentication** - Add proper auth for production use

### Code Execution Security
The CodeEngine tool executes arbitrary Python code. For production:
1. **Sandbox execution** - Use Docker containers or restricted environments
2. **Resource limits** - Implement CPU/memory/time constraints
3. **Network isolation** - Restrict network access from executed code
4. **File system isolation** - Use read-only or restricted file systems

### Dependencies
1. **Regular updates** - Keep all dependencies current
2. **Vulnerability scanning** - Use tools like `safety` or `pip-audit`
3. **Minimal dependencies** - Only include necessary packages

## Deployment Security Checklist

### Before Deployment
- [ ] Remove all hardcoded secrets
- [ ] Configure proper CORS origins
- [ ] Set up API key rotation
- [ ] Implement rate limiting
- [ ] Add input validation
- [ ] Set up logging and monitoring
- [ ] Configure HTTPS/SSL
- [ ] Test in isolated environment

### Production Environment
- [ ] Use environment-specific `.env` files
- [ ] Implement proper authentication
- [ ] Set up monitoring and alerting
- [ ] Configure backup and recovery
- [ ] Implement CI/CD security scanning
- [ ] Regular security audits

## Reporting Security Issues

If you discover a security vulnerability, please:
1. **Do not create a public issue**
2. Email security concerns to: [security@intelliflow.dev]
3. Include detailed reproduction steps
4. Allow reasonable time for response before public disclosure

## Security Tools Recommendations

### For Development
- `bandit` - Python security linter
- `safety` - Dependency vulnerability scanner
- `semgrep` - Static analysis security tool

### For Production
- Web Application Firewall (WAF)
- API Gateway with rate limiting
- Container security scanning
- Runtime security monitoring

## API Key Management

### Supported Providers
- **OpenAI**: Platform API for LLM capabilities
- **Traversaal Ares**: Internet search functionality
- **Perplexity**: Enhanced research capabilities
- **OpenRouter**: Alternative LLM provider access

### Key Security
- Store in environment variables only
- Use least-privilege access principles
- Monitor usage and set budgets
- Implement key rotation policies

## Update History
- **2025-01-XX**: Initial security audit and fixes
- Added comprehensive `.gitignore`
- Implemented environment variable validation
- Fixed CORS configuration
- Replaced unsafe `eval()` usage
