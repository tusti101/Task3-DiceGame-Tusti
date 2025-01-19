# Tusti Non-Transitive Dice Game 🎲

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A sophisticated implementation of a non-transitive dice game with provably fair random number generation using HMAC-based verification. This project demonstrates advanced concepts in cryptographic security, fair play mechanics, and object-oriented programming.

## 🌟 Features

- **Provably Fair Random Generation**: Uses HMAC-SHA3-256 for verifiable randomness
- **Colorful CLI Interface**: Enhanced user experience with color-coded outputs
- **Interactive Help System**: Detailed probability tables for game strategy
- **Robust Error Handling**: Comprehensive input validation and error messages
- **Flexible Dice Configuration**: Support for arbitrary number of dice (minimum 3)
- **Fair Play Mechanics**: Prevents duplicate dice selection between players

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/non-transitive-dice-game.git
cd non-transitive-dice-game
```

2. Create and activate virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on macOS/Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## 🎮 Usage

### Basic Game Launch

```bash
python dice.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3
```

### Command-Line Arguments

Each argument represents a die configuration with 6 comma-separated values:

```bash
python dice.py <die1_values> <die2_values> <die3_values> [additional_dice...]
```

### Example Configurations

1. Classic Example:

```bash
python dice.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3
```

2. Regular Dice:

```bash
python dice.py 1,2,3,4,5,6 1,2,3,4,5,6 1,2,3,4,5,6
```

## 🎯 Game Rules

1. The game starts by fairly determining the first player
2. First player selects a die from available options
3. Second player selects a different die
4. Both players roll their dice using provably fair random generation
5. Higher number wins the game
6. HMAC verification ensures fair play

## 🧪 Test Cases

### Valid Inputs

```bash
# Standard game with 3 dice
python dice.py 2,2,4,4,9,9 6,8,1,1,8,6 7,5,3,7,5,3

# Game with 4 identical dice
python dice.py 1,2,3,4,5,6 1,2,3,4,5,6 1,2,3,4,5,6 1,2,3,4,5,6
```

### Error Cases

```bash
# Too few dice
python dice.py 1,2,3,4,5,6

# Invalid dice values
python dice.py a,b,c,d,e,f 1,2,3,4,5,6 1,2,3,4,5,6

# Wrong number of values
python dice.py 1,2,3 4,5,6 7,8,9

# No parameters
python dice.py
```

## 🔍 Code Structure

```
non-transitive-dice-game/
├── dice.py           # Main game implementation
├── requirements.txt  # Project dependencies
├── LICENSE          # MIT license
└── README.md        # This file
```

### Key Classes

- `Dice`: Manages individual die configuration and validation
- `FairRandomGenerator`: Handles cryptographically secure random generation
- `Game`: Controls game flow and user interaction
- Additional utility classes for specific functionalities

## 🔐 Security Features

- 256-bit cryptographic keys
- HMAC-SHA3-256 for hash generation
- Verifiable random number generation
- Secure dice selection process

## 🎨 UI Features

- Color-coded output for better readability
- Interactive probability tables
- Clear error messages
- Intuitive menu system
- Progress indicators

## 📊 Probability Table Example

```
+----------+--------+--------+--------+
| User Dice| Dice 1 | Dice 2 | Dice 3 |
+----------+--------+--------+--------+
| Dice 1   |-0.3333 | 0.5556 | 0.4444 |
| Dice 2   | 0.4444 |-0.3333 | 0.5556 |
| Dice 3   | 0.5556 | 0.4444 |-0.3333 |
+----------+--------+--------+--------+
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Requirements

- Python 3.8 or higher
- prettytable
- colorama
- Virtual environment (recommended)

## 🐛 Troubleshooting

1. **Virtual Environment Issues**

   ```bash
   # If venv creation fails, try:
   python -m pip install --upgrade pip
   pip install virtualenv
   virtualenv venv
   ```
2. **Color Display Issues**

   ```bash
   # On Windows, if colors don't display:
   python -m pip install --upgrade colorama
   ```
3. **Permission Errors**

   ```bash
   # On Linux/macOS:
   chmod +x dice.py
   ```

## 📈 Future Improvements

- Network multiplayer support
- GUI interface
- Additional die configurations
- Statistical analysis tools
- Tournament mode
