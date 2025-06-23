# PI3a Bluetooth Simulator
The goal is to create a bluetooth device that mimics hardware input to an app.

## Dependencies
Initialize a Venv, then: pip install bless

## Activating Virtual Environment
Run: 'source venv/bin/activate'

## Running the BLE Simulator
Enter: 'python3 ble_stream.py'
Make sure to have the app you are testing send a '0x01' signal to the hardware to let it know to begin sending a stream of data
