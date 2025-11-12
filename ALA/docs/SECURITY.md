# Security Guidelines

## API Key Management

**IMPORTANT**: Never commit API keys, secrets, or credentials to the repository.

### Secure Credential Storage

1. **Use Environment Variables**
   ```bash
   export GOOGLE_API_KEY="your-actual-key-here"
   export ANTHROPIC_API_KEY="your-actual-key-here"
   ```

2. **Use .env Files (Not Committed)**
   - Create a `.env` file in your project root
   - Add `.env` to `.gitignore` (already configured)
   - Example `.env` file:
   ```bash
   GOOGLE_API_KEY=your-actual-key-here
   ANTHROPIC_API_KEY=your-actual-key-here
   OPENAI_API_KEY=your-actual-key-here
   ```

3. **Template Files**
   - Use `.env.example` or `config.example.json` as templates
   - Replace placeholder values with actual credentials locally
   - Never commit the actual credential files

### If You Accidentally Expose Credentials

If you accidentally commit credentials to the repository:

1. **Immediately revoke/regenerate the exposed credentials**
   - Go to the service provider's console (Google Cloud, OpenAI, etc.)
   - Delete or regenerate the compromised API key

2. **Remove from repository**
   ```bash
   # Remove the file from git tracking
   git rm --cached path/to/file

   # Or remove from git history entirely
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch path/to/file" \
     --prune-empty --tag-name-filter cat -- --all
   ```

3. **Update .gitignore** to prevent future commits

4. **Force push the cleaned history** (if already pushed)
   ```bash
   git push origin --force --all
   ```

### Best Practices

- ✅ Use environment variables for sensitive data
- ✅ Keep `.env` files in `.gitignore`
- ✅ Use example/template files with placeholder values
- ✅ Regularly rotate API keys
- ✅ Use different keys for development and production
- ❌ Never hardcode credentials in source code
- ❌ Never commit `.env` files
- ❌ Never share credentials in documentation

### Checking for Exposed Credentials

Run regular scans to check for exposed credentials:

```bash
# Check for potential API keys in files
grep -r "api[_-]key\|password\|secret\|token" --include="*.py" --include="*.sh" --include="*.md"

# Check git history for sensitive files
git log --all --full-history --source -- "*.env" "*secret*" "*credential*"
```

## Reporting Security Issues

If you discover a security vulnerability, please report it to the repository maintainers privately before disclosing publicly.
