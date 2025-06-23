# PI3a Bluetooth Simulator
Purpose: Program that has the pi device mimic an actual hardware device for bluetooth testing on an app--can be modified for other applications but for this program, I want a stream of batch numbers that mimic an EMG device
## Initialize and Activate Virtual Environment
Initialize: 'python -m venv venv'
Activate: 'source venv/bin/activate'

## Dependencies
Install BLESS Library: pip install bless

## Running the BLE Simulator
Run: 'python3 ble_stream.py'
Make sure to have the app you are testing send a '0x01' signal to the hardware.
This lets it know to begin sending a stream of data.
