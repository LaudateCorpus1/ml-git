"""
© Copyright 2020 HP Development Company, L.P.
SPDX-License-Identifier: GPL-2.0-only
"""

messages = [
    "INFO - Admin: Initialized empty ml-git repository in",  # 0
    "INFO - Admin: You already are in a ml-git repository",  # 1
    "INFO - Admin: Add remote repository [%s] for [dataset]",  # 2
    "INFO - Admin: Add remote repository [%s] for [labels]",  # 3
    "INFO - Admin: Add remote repository [%s] for [model]",  # 4
    "INFO - Admin: Changing remote from [%s]  to [%s] for  [dataset]",  # 5
    "ERROR - Admin: You are not in an initialized ml-git repository.",  # 6
    "INFO - Admin: Add store [s3h://%s] in region [us-east-1] with creds from profile [%s]",  # 7
    "INFO - Metadata Manager: Metadata init [%s] @ [%s]",  # 8
    "ERROR - Repository: The path [%s] already exists and is not an empty directory.",  # 9
    "ERROR - Repository: Unable to find %s. Check the remote repository used.",  # 10
    "ERROR - Repository: Unable to find remote repository. Add the remote first.",  # 11
    "INFO - Admin: Add remote repository [%s] for [model]",  # 12
    "INFO - Repository: dataset adding path",  # 13
    "INFO - Repository: model adding path",  # 14
    "INFO - Repository: labels adding path",  # 15
    "ERROR - Repository: The entity name passed is wrong. Please check again",  # 16
    "INFO - Metadata Manager: Commit repo[%s] --- file[%s]",  # 17
    "INFO - Local Repository: No blobs to push at this time.",  # 18
    "INFO - Repository: dataset adding path [%s] to ml-git index",  # 19
    "INFO - Metadata Manager: Pull [%s]",  # 20
    "ERROR - Local Repository: The amount parameter should be smaller than the group size.",  # 21
    "ERROR - Local Repository: The group size parameter should be smaller than the file list size.",  # 22
    "ERROR - Local Repository: The start parameter should be smaller than the stop.",  # 23
    "ERROR - Local Repository: The stop parameter should be smaller than or equal to the file list size.",  # 24
    "ERROR - Local Repository: The start parameter should be greater than or equal to zero.",  # 25
    "ERROR - Local Repository: The step parameter should be smaller than the stop.",  # 26
    "INFO - Repository: There is no new data to add",  # 27
    "ERROR - Local Repository: The group size parameter should be greater than zero.",  # 28
    "ERROR - Local Repository: The frequency  parameter should be greater than zero.",  # 29
    "ERROR - Local Repository: The amount parameter should be smaller than the frequency.",  # 30
    "ERROR - Local Repository: The frequency  parameter should be smaller than the file list size.",  # 31
    "ERROR - Local Repository: Requires positive integer values.",  # 32
    "ERROR - Admin: Permission denied. You need write permission to initialize ml-git in this directory.",  # 33
    "ERROR - Repository: You are not in an initialized ml-git repository.",  # 34
    "ERROR - MLGit: remote-fsck -- fixed   : ipld[0] / blob[1]", # 35
    "Total of corrupted files: %d",  # 36
    "INFO - Metadata Manager: Pull [%s]",  # 37
    "Project Created.",  # 38
    "Successfully loaded configuration files!",  # 39
    "ERROR - Local Repository: The --random-sample=<amount:frequency> --seed=<seed>: requires positive integer values.", #40
    "ERROR - Local Repository: The --group-sample=<amount:group-size> --seed=<seed>: requires positive integer values.", #41
    "ERROR - Local Repository: The --range-sample=<start:stop:step> or  --range-sample=<start:stop>: requires positive integer values." #42
]