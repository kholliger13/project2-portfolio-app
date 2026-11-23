#!/bin/sh
set -eu
cd "$(dirname "$0")"

python lab13_baselines.py
python verify_portfolio_app.py
python verify_asof.py
python payems_verify.py
python verify_rates_app.py
python verify_asof_app.py
python verify_claims.py && python verify_claims.py --self-test
