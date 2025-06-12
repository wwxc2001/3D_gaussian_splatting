import os
import argparse
from tensorboard import program

def launch_tensorboard(log_dir, port):
    tb = program.TensorBoard()
    tb.configure(argv=[None, '--logdir', log_dir, '--port', str(port)])
    url = tb.launch()
    print(f"TensorBoard is available at {url}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Launch TensorBoard for visualization")
    parser.add_argument('--log_dir', type=str, default="./output", help="Directory containing TensorBoard logs")
    parser.add_argument('--port', type=int, default=6006, help="Port to run TensorBoard on")
    args = parser.parse_args()

    launch_tensorboard(args.log_dir, args.port)