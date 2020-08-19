import lissandra as liss
from lissandra import ShardStatus


def get_shard():
    status = liss.get_status(region="NA")
    status = ShardStatus(region="NA")
    print(status.name)


if __name__ == "__main__":
    get_shard()
