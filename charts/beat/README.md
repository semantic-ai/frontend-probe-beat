# BeAT Helm Chart

Besluit Annotation Tool

## Introduction

This chart can be used to deploy an BeAT instance to a kubernetes cluster.

## Prerequisites

- Kubernetes 1.19+
- Helm 3.4.0+

## Installing the Chart

To install the chart with release name `my-beat`:

```bash
helm install my-beat .
```

You could port-forward the service to access the web UI at `127.0.0.1:5000`:

```bash
kubectl port-forward svc/my-mlflow 5000:80
```

## Uninstalling the Chart

To uninstall the `my-beat` release:

```bash
helm delete my-beat
```

The command removes all the Kubernetes components associated with the chart and deletes the release.

## Parameters

See `values.yaml` for all the helm chart parameters and descriptions

While installing the chart, specify each parameter using `--set key=value[,key=value]` arguments,
or provide a YAML file that specifies the values to override specific parameters, like so:

```bash
helm install my-beat /path/to/chart --values my-beat-values.yaml
```
