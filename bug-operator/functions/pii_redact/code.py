#input_type_name: PiiRedactInput
#output_type_name: PiiRedactOutput
#function_name: pii_redact

import re
from pydantic import BaseModel
from lemma_sdk import FunctionContext

class PiiRedactInput(BaseModel):
    title: str
    description: str

class PiiRedactOutput(BaseModel):
    title: str
    description: str
    redaction_count: int

REDACTION_PATTERNS = [
    # Bearer tokens / Authorization headers
    (r'(?i)(bearer\s+)[A-Za-z0-9\-._~+/]+=*', r'\1[REDACTED_TOKEN]'),
    # JWT tokens (three base64 segments)
    (r'eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+', '[REDACTED_JWT]'),
    # OpenAI / Anthropic / generic sk- API keys
    (r'(?i)(sk-|ak-|rk-)[A-Za-z0-9]{20,}', '[REDACTED_API_KEY]'),
    # Generic API key patterns: key=VALUE or api_key=VALUE
    (r'(?i)(api[_-]?key|access[_-]?token|secret[_-]?key|auth[_-]?token)(\s*[=:]\s*)([\'"]?)([A-Za-z0-9\-._~+/!@#$%^&*]{8,})([\'"]?)', r'\1\2\3[REDACTED]\5'),
    # Passwords
    (r'(?i)(password|passwd|pwd)(\s*[=:]\s*)([\'"]?)(\S+)([\'"]?)', r'\1\2\3[REDACTED]\5'),
    # Credit card numbers (Visa/MC/Amex/Discover)
    (r'\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b', '[REDACTED_CARD]'),
    # Private key blocks
    (r'-----BEGIN [A-Z ]+PRIVATE KEY-----.*?-----END [A-Z ]+PRIVATE KEY-----', '[REDACTED_PRIVATE_KEY]'),
    # AWS access keys
    (r'(?<![A-Z0-9])(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}', '[REDACTED_AWS_KEY]'),
    # Connection strings / DSN with passwords
    (r'(?i)(mongodb|postgres|mysql|redis|amqp):\/\/[^:]+:[^@]+@', r'\1://[REDACTED_CREDS]@'),
    # Email addresses embedded in log dumps (preserve first char for context)
    (r'(?<!\w)([a-zA-Z0-9._%+-]{1})[a-zA-Z0-9._%+-]+(@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r'\1***\2'),
]

def redact_text(text: str) -> tuple[str, int]:
    count = 0
    for pattern, replacement in REDACTION_PATTERNS:
        new_text, n = re.subn(pattern, replacement, text, flags=re.DOTALL)
        count += n
        text = new_text
    return text, count

async def pii_redact(ctx: FunctionContext, data: PiiRedactInput) -> PiiRedactOutput:
    clean_title, n1 = redact_text(data.title)
    clean_desc, n2 = redact_text(data.description)
    return PiiRedactOutput(
        title=clean_title,
        description=clean_desc,
        redaction_count=n1 + n2
    )
