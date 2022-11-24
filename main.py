from time import sleep
from re import search
import qbittorrentapi

def isBadClient(client):
    regex_list = [
        r"^-XL0012",
        r"^Xunlei",
        r"^7\."
    ]

    for regex in regex_list:
        if search(regex, client):
            return True

    return False

# Web UI 信息
qb_client = qbittorrentapi.Client(
    host="localhost",
    port=8080,
    username="admin",
    password="password"
)

try:
    qb_client.auth_log_in()
except qbittorrentapi.LoginFailed as e:
    print(e)

print(f"# qBittorrent: {qb_client.app.version}")
print(f"# qBittorrent Web API: {qb_client.app.web_api_version}")

# 清空旧的 IP 封禁列表
qb_client.app_set_preferences({ "banned_IPs": "" })

while True:
    for torrent in qb_client.torrents_info():
        try:
            peers_info = qb_client.sync_torrent_peers(torrent_hash=torrent.hash)
        except:
            break

        for k, peer in peers_info.peers.items():
            if (
              isBadClient(peer.client)
              and peer.up_speed > peer.dl_speed * 2
              and peer.uploaded > peer.downloaded
            ):
                qb_client.transfer_ban_peers(k)
                print(f">> ban: {k} \"{peer.client}\"")

    sleep(5)
