# PI3a Bluetooth Simulator
The goal is to create a bluetooth device that mimics hardware input to an app.

## Initialize and Activate Virtual Environment
Initialize: 'python -m venv venv'
Activate: 'source venv/bin/activate'

## Dependencies
Install BLESS Library: pip install bless

## Running the BLE Simulator
Run: 'python3 ble_stream.py'
Make sure to have the app you are testing send a '0x01' signal to the hardware.
This lets it know to begin sending a stream of data.
