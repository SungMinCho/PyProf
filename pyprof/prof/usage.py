#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import argparse


def parseArgs():
    """
	Print usage and parse arguments.
	"""

    def check_cols(value):
        valid = [
            "idx", "seq", "altseq", "tid", "layer", "trace", "dir", "sub", "mod", "op", "kernel", "kernel_long", "params", "sil", "tc",
            "device", "stream", "grid", "block", "flops", "bytes"
        ]
        cols = value.split(",")
        for col in cols:
            if col not in valid:
                raise argparse.ArgumentTypeError(
                    "{} is not a valid column name. Valid column names are {}.".format(col, ",".join(valid))
                )
        return cols

    def openFile(f):
        try:
            d = open(f, "r")
            return d
        except IOError:
            print("Error opening file {}. Exiting.".format(f), file=sys.stderr)
            sys.exit(1)

    parser = argparse.ArgumentParser(
        prog=sys.argv[0], description="PyTorch Profiler", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("file", nargs='?', type=str, default=None, help="Output of parse.py (Python dictionary).")

    parser.add_argument(
        "-c", type=check_cols, default="idx,dir,sub,mod,op,kernel,kernel_long,params,sil",
        help='''Comma seperated names of columns to print.
idx:      Index
seq:      PyTorch Sequence Id
altseq:   PyTorch Alternate Sequence Id
tid:      Thread Id
layer:    User annotated NVTX string (can be nested)
trace:    Function Call Trace
dir:      Direction
sub:      Sub Sequence Id
mod:      Module
op:       Operattion
kernel:   Kernel Name
params:   Parameters
sil:      Silicon Time (in ns)
tc:       Tensor Core Usage
device:   GPU Device Id
stream:   Stream Id
grid:     Grid Dimensions
block:    Block Dimensions
flops:    Floating point ops (FMA = 2 FLOPs)
bytes:    Number of bytes in and out of DRAM
e.g. -c idx,kernel,sil'''
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--csv", action="store_true", default=False, help="Print a CSV output.")
    group.add_argument("-w", type=int, default=0, help="Width of columnated output.")

    args = parser.parse_args()
    if args.file is None:
        args.file = sys.stdin
    else:
        args.file = openFile(args.file)
    return args
