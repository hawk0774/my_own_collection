# Yandex Cloud ELK — Test Collection

## Content
- **Module**: `my_own_module` — creates file 
- **Role**: `create_file` — uses `my_own_module` with defaults

## Role: `create_file`

```yaml
- role: my_own_namespace.yandex_cloud_elk.create_file
  vars:
    my_own_module_path: /tmp/custom.txt
