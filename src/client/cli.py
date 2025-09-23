import argparse
from typing import Optional
from src.services.device_service import DeviceService
from src.services.home_controller_service import HomeControllerService


def main():
    parser = argparse.ArgumentParser(prog="homeauto", description="Home Automation CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # create device
    p_create = sub.add_parser("create-device")
    p_create.add_argument("type")
    p_create.add_argument("name")
    p_create.add_argument("location")
    p_create.add_argument("user_id", type=int)
    p_create.add_argument("--on", action="store_true")

    # list devices for user
    p_list = sub.add_parser("list-devices")
    p_list.add_argument("user_id", type=int)

    # control
    p_on = sub.add_parser("on")
    p_on.add_argument("device_id", type=int)
    p_off = sub.add_parser("off")
    p_off.add_argument("device_id", type=int)

    args = parser.parse_args()
    devices = DeviceService()
    ctrl = HomeControllerService()

    if args.cmd == "create-device":
        created = devices.create(args.type, args.name, args.on, args.location, args.user_id)
        print(created)
    elif args.cmd == "list-devices":
        print(ctrl.list_user_devices(args.user_id))
    elif args.cmd == "on":
        print(devices.control_on(args.device_id))
    elif args.cmd == "off":
        print(devices.control_off(args.device_id))


if __name__ == "__main__":
    main()

