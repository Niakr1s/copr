# Description

This repo contains some extra packages for my daily usage.

## Reminders for myself

This repo should be placed in `~/rpmbuild`.
Packages can be build locally using `rpmbuild -bb ~/rpmbuild/SPECS/<pkg>.spec`.
The contents of the package can be shown using `rpm -qlp ~/rpmbuild/RPMS/x86_64/<pkg>.rpm`.

## Obtaining sources

There is a script `srcdl.sh`, that is being mantained and downloads needed
tarballs to `~/rpmbuild/SOURCES` directory.

## Building

There is a script `build.sh`, that builds all specs to a source RPM.

### Partial building

For testing, you can skip build phase.

- First build full build:

```bash
rpmbuild --noclean -bb <pkg>.spec
```

- Edit your .spec file (e.g., tweaking %install, %files, or .service) and rerun:

```bash
rpmbuild --noclean --short-circuit -bi <pkg>.spec # to rerun install phase
rpmbuild --noclean --short-circuit -bb <pkg>.spec # to make rpm
```

- You can install partially built rpm, using:

```bash
sudo rpm -Uvh --nodeps RPMS/x86_64/llama-cpp-cmpfix-1.0.0-1.fc44.x86_64.rpm
```

## Upload to copr repo

You need to build a source rpm and then build it remotely using copr-cli.

```bash
# download sources
spectool -g -R ~/rpmbuild/SPECS/<pkg>.spec
# build a source rpm
rpmbuild -bs ~/rpmbuild/SPECS/<pkg>.spec
# push to cloud
copr-cli build <owner>/<repo> ~/rpmbuild/SRPMS/<pkg>.src.rpm
```

## Packages

- **nvidia-pstated**:
Automatically manages idle states of Nvidia GPUs.

- joystickwake:
Prevents the system from sleeping while using gamepad.

- llama-cpp-cmpfix:
A llama.cpp with D4PA disabled, that considerably improves generation speed
on mining nvidia GPUs.
