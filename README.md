# T20 Cricket Score Prediction Model

A machine learning model to predict powerplay (first 6 overs) scores in T20 cricket matches. This project achieved a top 50 placement in an academic competition.

## Overview

This model predicts the score at the end of the first 6 overs (powerplay) in T20 cricket matches using historical match data and advanced machine learning techniques.

## Features

### Data Analysis
- Comprehensive analysis of historical T20 cricket match data
- Feature engineering based on key cricket metrics
- Data preprocessing and cleaning pipelines

### Model Architecture
- Machine learning model optimized for cricket score prediction
- Integration of multiple relevant features:
  - Team performance history
  - Player statistics
  - Venue information
  - Match conditions
  - Historical powerplay trends

### Technical Implementation

### Core Components

1. Data Processing (`IPLDataProcessor` class)
   - Standardizes venue names across datasets
   - Cleans and merges ball-by-ball and match data
   - Handles team name standardization
   - Removes defunct teams and invalid matches
   - Creates aggregated pivot tables for analysis

2. Prediction Model (`IPLPredictor` class)
   - Implements multiple strike rate calculations:
     - Batsman vs specific bowler
     - Batsman performance at venues
     - Innings-specific performance
   - Uses weighted averaging for final predictions
   - Factors in team and opposition statistics

3. Implementation Features
   - Type hints for better code reliability
   - Comprehensive error handling
   - Model serialization support
   - Modular and maintainable architecture
   - Unit-testable components

## Project Structure

```
├── data/                    # Data files and datasets
│   ├── IPL_Ball_by_Ball_2008_2022.csv
│   └── IPL_Matches_2008_2022.csv
├── models/                  # Saved model files
│   └── ipl_predictor_model.pkl
├── src/                    # Source code
│   ├── __init__.py
│   ├── ipl_predictor.py    # Main predictor implementation
│   └── utils.py           # Utility functions
├── tests/                  # Unit tests
│   └── test_predictor.py
├── requirements.txt        # Project dependencies
└── README.md              # Project documentation
```

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Initialize the data processor:
```python
from ipl_predictor import IPLDataProcessor

processor = IPLDataProcessor(
    ball_by_ball_path='IPL_Ball_by_Ball_2008_2022.csv',
    matches_path='IPL_Matches_2008_2022.csv'
)
```

2. Create and use the predictor:
```python
from ipl_predictor import IPLPredictor

predictor = IPLPredictor(processor)

# Example prediction
prediction = predictor.predict_score(
    batsmen=['V Kohli', 'F du Plessis'],
    bowlers=['TA Boult', 'R Ashwin', 'Avesh Khan'],
    venue='M Chinnaswamy Stadium',
    innings=2,
    batting_team='Royal Challengers Bangalore',
    bowling_team='Rajasthan Royals'
)
```

## Model Performance

- Achieved top 50 placement in academic competition
- Prediction Algorithm:
  - Uses weighted combination of multiple factors:
    - Individual batsman-bowler matchups (65% weight)
    - Venue-specific performance (30% weight)
    - Innings-specific statistics (5% weight)
  - Incorporates team averages and opposition bowling statistics
  - Accounts for extras and team-specific patterns
  - Adjusts predictions based on current season performance

## Future Improvements

- Integration of real-time weather data
- Enhanced feature engineering
- Deep learning model variants
- API development for real-time predictions

## Acknowledgments

- Academic competition organizers
- Cricket data providers
- Open-source community for various tools and libraries used
-----
