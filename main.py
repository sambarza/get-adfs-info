import argparse
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


def format_size(size_bytes: int) -> str:
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} PB"


def get_container_size(client: BlobServiceClient, container_name: str) -> int:
    container_client = client.get_container_client(container_name)
    return sum(blob.size for blob in container_client.list_blobs())


def list_blob_containers(storage_account_name: str) -> None:
    account_url = f"https://{storage_account_name}.blob.core.windows.net"
    credential = DefaultAzureCredential()
    client = BlobServiceClient(account_url=account_url, credential=credential)

    print(f"Containers in storage account '{storage_account_name}':")
    containers = list(client.list_containers())
    if not containers:
        print("  (no containers found)")
        return
    for container in containers:
        name = container["name"]
        size = get_container_size(client, name)
        print(f"  - {name:<40} {format_size(size)}")


def main():
    parser = argparse.ArgumentParser(description="List blob containers in an Azure Storage account")
    parser.add_argument("--storage-account", required=True, help="Name of the Azure Storage account")
    args = parser.parse_args()
    list_blob_containers(args.storage_account)


if __name__ == "__main__":
    main()
