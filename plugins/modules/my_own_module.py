#!/usr/bin/python
# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_own_module
short_description: Creates a file only if it does not exist
description: |
  This module creates a text file at the given path with specified content,
  but only if the file does not already exist. Existing files are never modified.
version_added: "1.0.0"
options:
  path:
    description: Full path to the file to create.
    required: true
    type: str
  content:
    description: Content to write to the file (only if file is missing).
    required: true
    type: str
  mode:
    description: File permissions in octal notation (e.g. 0644).
    required: false
    type: str
    default: '0644'
author:
  - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
- name: Create initial log entry
  my_namespace.my_collection.my_test:
    path: /var/log/myapp/first_run.txt
    content: "First run completed at {{ ansible_date_time.iso8601 }}\n"
    mode: '0644'

- name: Ensure placeholder file exists
  my_namespace.my_collection.my_test:
    path: /etc/myapp/PLACEHOLDER
    content: "# This is a placeholder\n"
'''

RETURN = r'''
path:
  description: The target file path.
  type: str
  returned: always
  sample: /tmp/example.txt
content:
  description: The content that was (or would be) written.
  type: str
  returned: always
created:
  description: Whether the file was created during this run.
  type: bool
  returned: always
  sample: true
'''

from ansible.module_utils.basic import AnsibleModule
import os

def write_file(path, content, mode):
    """Write content and set file mode."""
    with open(path, 'w') as f:
        f.write(content)
    os.chmod(path, int(mode, 8))

def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=True),
        mode=dict(type='str', default='0644')
    )

    result = dict(
        created=False,
        path='',
        content=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    path = module.params['path']
    content = module.params['content']
    mode = module.params['mode']

    # Validate mode format
    try:
        int(mode, 8)
    except ValueError:
        module.fail_json(msg=f"Invalid mode '{mode}'. Use octal format like '0644'.")

    result['path'] = path
    result['content'] = content

    # Check if parent directory exists
    dirname = os.path.dirname(path)
    if dirname and not os.path.isdir(dirname):
        module.fail_json(
            msg=f"Parent directory does not exist: {dirname}",
            **result
        )

    # Check if file already exists
    if os.path.exists(path):
        result['created'] = False
        module.exit_json(**result)

    # File does not exist → create it
    result['created'] = True

    if module.check_mode:
        module.exit_json(**result)

    # Write the file
    try:
        write_file(path, content, mode)
    except Exception as e:
        module.fail_json(msg=f"Failed to create file '{path}': {str(e)}", **result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
