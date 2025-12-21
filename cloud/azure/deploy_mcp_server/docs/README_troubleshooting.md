# Troubleshooting


## Opentelemtry dependency issue

Getting this error:

```bash
File "/tmp/azure/deploy_mcp_server/.venv/lib/python3.13/site-packages/azure/monitor/opentelemetry/__init__.py", line 7, in <module>
    from azure.monitor.opentelemetry._configure import configure_azure_monitor
  File "/tmp/azure/deploy_mcp_server/.venv/lib/python3.13/site-packages/azure/monitor/opentelemetry/_configure.py", line 27, in <module>
    from azure.monitor.opentelemetry._constants import (
    ...<15 lines>...
    )
  File "/tmp/azure/deploy_mcp_server/.venv/lib/python3.13/site-packages/azure/monitor/opentelemetry/_constants.py", line 7, in <module>
    from azure.monitor.opentelemetry.exporter._constants import (  # pylint: disable=import-error,no-name-in-module
        _AZURE_MONITOR_DISTRO_VERSION_ARG,
    )
  File "/tmp/azure/deploy_mcp_server/.venv/lib/python3.13/site-packages/azure/monitor/opentelemetry/exporter/__init__.py", line 7, in <module>
    from azure.monitor.opentelemetry.exporter.export.logs._exporter import AzureMonitorLogExporter
  File "/tmp/azure/deploy_mcp_server/.venv/lib/python3.13/site-packages/azure/monitor/opentelemetry/exporter/export/logs/_exporter.py", line 14, in <module>
    from opentelemetry.sdk._logs import LogData
ImportError: cannot import name 'LogData' from 'opentelemetry.sdk._logs' (/tmp/azure/deploy_mcp_server/.venv/lib/python3.13/site-packages/opentelemetry/sdk/_logs/__init__.py)
```

see [ImportError: cannot import name 'LogData' from 'opentelemetry.sdk._logs' in v1.8.2](https://github.com/azure/azure-sdk-for-python/issues/44237)

