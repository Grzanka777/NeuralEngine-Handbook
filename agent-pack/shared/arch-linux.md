# Arch Linux Diagnostics

Use this skill when diagnosing Arch Linux, CachyOS, systemd, kernel, hardware, storage, Wayland, graphics, networking, package, boot, or performance problems.

Begin with evidence collection. Do not modify the system before establishing the current state.

## Core principles

Always:

* distinguish observation from interpretation;
* distinguish evidence from hypothesis;
* prefer read-only diagnostics first;
* use the smallest relevant command set;
* preserve exact command output when it supports a conclusion;
* explain uncertainty;
* propose reversible changes before permanent ones.

Do not:

* guess the root cause from one symptom;
* recommend destructive commands without explicit authorization;
* reinstall components before diagnosing them;
* disable security controls merely to bypass an error;
* treat community anecdotes as authoritative evidence;
* claim success without verification.

## NeuralEngine usage

At the start of work, follow the mandatory global NeuralEngine instructions.

Run:

```text
neural status
```

Determine whether prior system knowledge, decisions, experience, or playbooks are relevant.

When relevant:

1. run `neural search`;
2. record the exact query;
3. record returned record IDs and provenance;
4. explain how the result affected the diagnostic path.

When repository files, current logs, or direct system evidence are sufficient:

1. state that no NeuralEngine search was required;
2. explain why current evidence was sufficient.

Running only `neural status` does not constitute NeuralEngine knowledge use.

Any Brain write requires:

1. a preview of the proposed record;
2. explicit user authorization;
3. no automatic lifecycle promotion.

## Diagnostic sequence

Follow this order unless the problem requires a narrower path.

### 1. Define the symptom

Establish:

* what failed;
* when it started;
* whether it is reproducible;
* whether it affects every boot or only some sessions;
* what changed recently;
* whether the issue is local, user-session, system-wide, hardware-specific, or network-specific.

Do not ask for information already available from logs or commands.

### 2. Establish system context

Use only relevant commands.

Typical baseline:

```text
uname -a
cat /etc/os-release
uptime
systemctl --failed
journalctl -b -p warning
```

For kernel and boot:

```text
cat /proc/cmdline
journalctl -b -k
systemd-analyze
systemd-analyze blame
```

For hardware:

```text
lspci -k
lsusb
inxi -Fazy
```

Do not require `inxi` when it is not installed and standard tools are sufficient.

### 3. Collect subsystem evidence

Choose only the applicable section.

## systemd services

Use:

```text
systemctl status <unit>
systemctl show <unit>
journalctl -b -u <unit>
journalctl -xeu <unit>
systemctl cat <unit>
```

Differentiate:

* unit configuration;
* dependency failure;
* execution failure;
* timeout;
* permission failure;
* missing executable;
* environment failure.

Do not recommend `daemon-reload`, restart, enable, disable, mask, or reset-failed until the current unit state and configuration are understood.

## Kernel and hardware

Use:

```text
journalctl -b -k
dmesg --level=err,warn
lspci -nnk
lsmod
modinfo <module>
```

For suspected hardware errors, inspect relevant evidence such as:

```text
journalctl -b -k | grep -Ei 'error|fail|reset|timeout|hang|oom|taint|mce|edac|nvme|btrfs|amdgpu|i915'
```

Do not conclude hardware failure solely from one warning.

## Graphics, niri, and Wayland

Use where applicable:

```text
niri msg outputs
niri validate
journalctl --user -b
journalctl --user -b -u niri
loginctl session-status
echo $XDG_SESSION_TYPE
echo $WAYLAND_DISPLAY
```

Inspect relevant configuration:

```text
sed -n '1,260p' ~/.config/niri/config.kdl
```

For Intel graphics:

```text
lspci -k | grep -A 4 -Ei 'vga|display'
journalctl -b -k | grep -Ei 'i915|xe|drm'
```

For AMD graphics:

```text
lspci -k | grep -A 4 -Ei 'vga|display'
journalctl -b -k | grep -Ei 'amdgpu|drm'
```

Do not suggest changing kernel parameters before identifying the active driver and relevant log evidence.

## Storage and filesystems

Use:

```text
lsblk -f
findmnt
findmnt -T <path>
df -hT
df -i
```

For Btrfs:

```text
sudo btrfs filesystem usage <mountpoint>
sudo btrfs device stats <mountpoint>
sudo btrfs scrub status <mountpoint>
```

Read-only commands requiring `sudo` are allowed only when needed and should be identified as privileged.

Before changing mounts, labels, ownership, permissions, subvolumes, or filesystem layout, establish:

* device;
* filesystem;
* mountpoint;
* current options;
* ownership;
* affected data;
* backup state.

Do not run:

```text
mkfs
wipefs
btrfs subvolume delete
rm -rf
parted
fdisk
```

without explicit authorization and a verified backup and rollback plan.

## Package management

Use:

```text
pacman -Qs <package>
pacman -Qi <package>
pacman -Qkk <package>
pacman -Qo <path>
pacman -Qm
```

For upgrade state:

```text
checkupdates
pacman -Qu
```

Do not perform partial upgrades.

Do not use `pacman -Sy` without a full upgrade context.

Before reinstalling packages, inspect package integrity and ownership.

## Networking

Use:

```text
ip address
ip route
resolvectl status
networkctl status
ss -tulpn
ping -c 4 <host>
```

Choose either NetworkManager or systemd-networkd diagnostics based on the active stack.

For NetworkManager:

```text
nmcli general status
nmcli device status
journalctl -b -u NetworkManager
```

For systemd-networkd:

```text
networkctl
journalctl -b -u systemd-networkd
```

Do not change DNS, routes, firewall rules, or interfaces before capturing the current configuration.

## Performance and resource usage

Use:

```text
free -h
vmstat 1 5
ps aux --sort=-%mem
ps aux --sort=-%cpu
systemd-cgtop
```

For pressure and memory:

```text
cat /proc/pressure/cpu
cat /proc/pressure/memory
cat /proc/pressure/io
journalctl -b -k | grep -Ei 'oom|out of memory|killed process'
```

For disk latency:

```text
iostat -xz 1 5
```

Do not require tools that are not installed when equivalent standard evidence is available.

## Change boundary

Before suggesting a modifying command, provide:

1. expected effect;
2. affected files or services;
3. risk;
4. backup or snapshot requirement;
5. rollback command or procedure;
6. verification command.

Classify changes as:

* reversible session change;
* reversible configuration change;
* service-state change;
* package change;
* kernel or boot change;
* filesystem or partition change;
* destructive change.

Kernel, bootloader, initramfs, filesystem, partition, mount, security, or data-affecting changes require explicit user authorization.

## Command presentation

Separate commands into sections:

### Read-only diagnostics

Commands that inspect state only.

### Proposed changes

Commands that modify configuration, services, packages, files, or state.

### Verification

Commands proving whether the change worked.

### Rollback

Commands or steps restoring the previous state.

Use fish-compatible syntax where possible.

Do not combine diagnostics and modification into one opaque command chain.

## Evidence classification

Label conclusions when useful:

* `[Certain]` — directly supported by current evidence;
* `[Likely]` — best explanation supported by multiple observations;
* `[Guessing]` — plausible but insufficiently supported.

Do not use confidence labels as a substitute for evidence.

## Required diagnostic report

Use this structure:

# Diagnostic report

## Primary finding

State the most important confirmed fact, risk, or missing evidence.

## System context

Include relevant:

* OS;
* kernel;
* session type;
* hardware;
* subsystem;
* affected service or path.

## Evidence

List exact commands and the relevant output or result.

## Interpretation

Separate:

* confirmed facts;
* likely causes;
* unresolved hypotheses.

## Proposed action

Provide:

* smallest reversible next step;
* expected effect;
* risk;
* required authorization.

## Verification

State how to confirm whether the action worked.

## Rollback

Provide rollback when a change is proposed.

## NeuralEngine usage

Provide the mandatory usage evidence.

## Verdict

Use one of:

* `DIAGNOSED`
* `LIKELY CAUSE IDENTIFIED`
* `INSUFFICIENT EVIDENCE`
* `BLOCKED`
* `RESOLVED`

Do not use `RESOLVED` without successful verification.
