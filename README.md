# Secure Password Generator

[![Python](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub last commit](https://img.shields.io/github/last-commit/robertojrss/secure-password-generator)](https://github.com/robertojrss/secure-password-generator/commits)
[![GitHub repo size](https://img.shields.io/github/repo-size/robertojrss/secure-password-generator)](https://github.com/robertojrss/secure-password-generator)
[![GitHub top language](https://img.shields.io/github/languages/top/robertojrss/secure-password-generator)](https://github.com/robertojrss/secure-password-generator)
[![Code style](https://img.shields.io/badge/code%20style-pep8-black)](https://www.python.org/dev/peps/pep-0008/)

A cryptographically secure password generator with entropy analysis and strength evaluation. Built with Python's `secrets` module for production-ready security.

## Features

[![Security](https://img.shields.io/badge/security-cryptographic-red.svg)](#)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)](#)
[![No Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen.svg)](#)

- **Cryptographically secure** random generation using Python's `secrets` module
- **Entropy calculation** based on character set size and password length
- **Strength evaluation** with 5 levels (Very Weak to Very Strong)
- **Crack time estimation** from seconds to trillions of years
- **Common password detection** against a database of breached passwords
- **Pattern analysis** to identify weak patterns (single character class, etc.)
- **Customizable character sets** (lowercase, uppercase, numbers, special chars)
- **User-friendly CLI** with input validation

## Installation

[![Clone](https://img.shields.io/badge/clone-https%3A%2F%2Fgithub.com%2Frobertojrss%2Fsecure--password--generator.git-orange)](https://github.com/robertojrss/secure-password-generator.git)

```bash
# Clone the repository
git clone https://github.com/robertojrss/secure-password-generator.git

# Navigate to the directory
cd secure-password-generator

# No additional dependencies required - uses only Python standard library
