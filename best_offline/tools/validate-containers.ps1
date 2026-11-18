param(
    [ValidateSet('rhel7', 'rhel9', 'all')]
    [string]$Target = 'all'
)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$workspaceRoot = Split-Path -Parent $projectRoot
$targets = @{
    rhel7 = @{
        Image = 'registry.access.redhat.com/ubi7/python-36@sha256:592b341772926e0617dd3b4fd40354640340e1f900090a682c8c3cea64b025e1'
        Python = '/opt/rh/rh-python36/root/usr/bin/python3.6'
        Version = '3.6'
        Wheelhouse = 'rhel7_python36_wheelhouse'
    }
    rhel9 = @{
        Image = 'registry.access.redhat.com/ubi9/python-39@sha256:447a4c9f6ead4f063bed8778793ac9e972004e5a55d103b375de83c885887e50'
        Python = '/usr/bin/python3.9'
        Version = '3.9'
        Wheelhouse = 'rhel9_python39_wheelhouse'
    }
}
$selectedTargets = if ($Target -eq 'all') { @('rhel7', 'rhel9') } else { @($Target) }
foreach ($targetName in $selectedTargets) {
    $spec = $targets[$targetName]
    # Constants above are controlled values; the Windows path is a separate argument.
    $command = '{0} tools/install-offline.py {1} /tmp/verified-env && /tmp/verified-env/bin/python tools/validate-target.py build/verified-{2} --expected-python {3} --container-network-none' -f $spec.Python, $spec.Wheelhouse, $targetName, $spec.Version
    & podman run --rm --pull=never --network none --arch amd64 --volume ($workspaceRoot + ':/workspace') --workdir /workspace/best_offline $spec.Image bash -c $command
    if ($LASTEXITCODE -ne 0) { throw "Validation failed for $targetName" }
}
