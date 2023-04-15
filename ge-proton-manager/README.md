# GE Proton Manager

## Fetch latest GE Proton every day

Put the `ge-proton-manager.service` and `ge-proton-manager.timer` files into `/home/deck/.config/systemd/user/` and enable the systemd timer:
```
cp ge-proton-manager.service ge-proton-manager.timer /home/deck/.config/systemd/user/

systemctl --user daemon-reload
systemctl --user start ge-proton-manager.timer
systemctl --user enable ge-proton-manager.timer
```
