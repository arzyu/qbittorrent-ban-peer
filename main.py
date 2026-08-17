from time import sleep
from re import search
import qbittorrentapi
from sys import exit
import argparse

def set_params_from_cmd():

    parser = argparse.ArgumentParser(prog='qbittorrent-ban-peer',
                                     description='Ban XunLei and similar peers using qBitorrent Web API',
                                     epilog="",
                                     add_help=False,
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--user', type=str,
                        default="admin",
                        help="Username for qBittorrent Web login")
    parser.add_argument('-p', '--password', required=True, type=str,
                        help="Password for qBittorrent Web login")
    parser.add_argument('-H', '--host', type=str,
                        default="localhost",
                        help="Host address to connect")
    parser.add_argument('-P', '--port',
                        type=int,
                        default=8080,
                        help="Port to connect to")
    parser.add_argument('-h', '--help',
                        action='help',
                        default=argparse.SUPPRESS,
                        help='Show this help message and exit.')
    return parser.parse_args()

def isBadClient(client):
    regex_list = [
        r"(?i)^-XL00",
        r"(?i)^Xunlei",
        r"^7\."
    ]

    for regex in regex_list:
        if search(regex, client):
            return True

    return False


try:
    args = set_params_from_cmd()
    # Web UI 信息
    qb_client = qbittorrentapi.Client(
        host=args.host,
        port=args.port,
        username=args.user,
        password=args.password
    )

    try:
        qb_client.auth_log_in()
    except qbittorrentapi.LoginFailed as e:
        print(f"Login failed. Check Username/Password")
        exit()
    except qbittorrentapi.Forbidden403Error as e:
        print(e)
        exit()
    except qbittorrentapi.APIConnectionError as e:
        print(e)
        exit()

    print("# Logged-in Successfully...")
    print(f"# qBittorrent: {qb_client.app.version}")
    print(f"# qBittorrent Web API: {qb_client.app.web_api_version}")

    # 清空旧的 IP 封禁列表
    qb_client.app_set_preferences({ "banned_IPs": "" })

    while True:
        for torrent in qb_client.torrents_info():
            try:
                peers_info = qb_client.sync_torrent_peers(torrent_hash =
                                                          torrent.hash)
            except:
                break

            for k, peer in peers_info.peers.items():
                if (
                  isBadClient(peer.client)
                  #and peer.up_speed > peer.dl_speed * 2
                  #and peer.uploaded > peer.downloaded
                ):
                    qb_client.transfer_ban_peers(k)
                    print(f">> ban: {k} \"{peer.client}\" from \
\"{torrent.name}\"")

        sleep(5)

except KeyboardInterrupt:
    exit(0)
