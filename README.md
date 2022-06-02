# Eye_Movement_Detection

## Installation instructions

#### Installing dependencies:

```shell
conda create -n bci python=3.9
conda activate bci
pip install -r requirements.txt
```

After installing, comment out the ```await asyncio.wait_for(event.wait(), timeout=timeout)``` line to avoid TimeoutError. 
Line 268 in anaconda3/envs/bci/Lib/site-packages/bleak/backends/winrt/client.py.
