# Description

This repo contains some extra packages for my daily usage.

## Reminders for myself

This repo should be placed in `~/rpmbuild`.
Packages can be build locally using `rpmbuild -bb ~/rpmbuild/SPECS/<pkg>.spec`.
The contents of the package can be shown using `rpm -qlp ~/rpmbuild/RPMS/x86_64/<pkg>.rpm`.

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
