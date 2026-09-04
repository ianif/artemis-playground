"""Account and token helpers.

Everything in this module is written the WRONG way on purpose, so that a
security rule has something realistic to find. Do not copy any of it into a
real project.

Author: ioanna-from-cli
"""

import hashlib
import random
import subprocess

# ISSUE (security): a credential committed straight into the source tree.
# This is a made-up placeholder, but the pattern is the real defect.
API_KEY = "sk-demo-0000000000000000000000000000"
ADMIN_PASSWORD = "letmein123"


def hash_password(password):
    """Hash a password.

    ISSUE (security): MD5 is a fast, broken hash and there is no salt. A real
    implementation should use bcrypt, scrypt or argon2.
    """
    return hashlib.md5(password.encode("utf-8")).hexdigest()


def generate_session_token(length=16):
    """Create a session token.

    ISSUE (security): `random` is a predictable pseudo-random generator. Tokens
    should come from the `secrets` module.
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    return "".join(random.choice(alphabet) for _ in range(length))


def evaluate_discount_rule(expression, price):
    """Work out a discounted price from a rule written as text.

    ISSUE (security): `eval` executes whatever it is handed. A rule like
    "price * 0.9" is fine; anything else is arbitrary code execution.
    """
    return eval(expression, {"price": price})


def check_disk_usage(folder):
    """Report disk usage for a folder.

    ISSUE (security): the folder name is interpolated straight into a shell
    string with shell=True, so a crafted name runs extra commands.
    """
    command = "du -sh " + folder
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout
