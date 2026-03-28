#!/usr/bin/env python
"""
Use Playwright Codegen to record actions and generate code automatically

Run with: source venv/bin/activate && python codegen_test.py
This opens a recording browser where every action generates Playwright code
"""
import subprocess
import sys

print("\n" + "="*70)
print("PLAYWRIGHT CODEGEN - Browser Recording Tool")
print("="*70)
print("\nThis will open a browser where every action is recorded as code.\n")

print("STEPS:")
print("1. Browser will open to SITRAM portal")
print("2. Do this sequence:")
print("   a) Fill Start Date: 01/12/2025")
print("   b) Fill End Date: 31/12/2025")
print("   c) Fill CNPJ: 23602073000159 (or 23.602.073/0001-59)")
print("   d) Click Search button")
print("   e) Wait for results")
print("   f) Click CSV button to download")
print("\n3. In the Inspector panel on the right, you'll see generated Playwright code")
print("4. Copy the code to the clipboard")
print("5. Close the browser (Codegen will exit)\n")

print("Starting Playwright Codegen...")
print("-"*70 + "\n")

# Run playwright codegen
cmd = [
    sys.executable, "-m", "playwright", "codegen",
    "https://portal-sitram.sefaz.ce.gov.br/sitram-internet/#/pagamento-icms/por-nota-fiscal/fiscal",
    "--output", "/tmp/sitram_recorded.py"
]

try:
    subprocess.run(cmd, check=False)
except KeyboardInterrupt:
    print("\n\nCodegen stopped.")

print("\n" + "-"*70)
print("If code was recorded, it will be saved to: /tmp/sitram_recorded.py")
print("="*70 + "\n")
