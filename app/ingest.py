from pathlib import Path
from urllib.request import Request, urlopen


RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


DOCUMENTS = [
    # NIST AI
    {
        "name": "nist_ai_rmf",
        "url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
    },
    {
        "name": "nist_genai_profile",
        "url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf",
    },

    # NIST Cybersecurity Framework
    {
        "name": "nist_csf_2_0",
        "url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
    },
    {
        "name": "nist_csf_overview",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.1299.pdf",
    },

    # NIST Privacy
    {
        "name": "nist_privacy_framework",
        "url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.40.ipd.pdf",
    },

    # NIST Zero Trust
    {
        "name": "nist_zero_trust",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf",
    },

    # NIST Risk Management
    {
        "name": "nist_rmf",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-37r2.pdf",
    },
    {
        "name": "nist_risk_assessment",
        "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-30r1.pdf",
    },

    # NIST Security Controls
    {
        "name": "nist_security_controls",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-53r5.pdf",
    },

    # NIST Incident Response
    {
        "name": "nist_incident_response",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r2.pdf",
    },

    # NIST Secure Software Development
    {
        "name": "nist_ssdf",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf",
    },

    # NIST Supply Chain
    {
        "name": "nist_supply_chain",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-161r1.pdf",
    },

    # NIST Systems Security Engineering
    {
        "name": "nist_system_security_engineering",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-160v1r1.pdf",
    },

    # NIST Security Testing
    {
        "name": "nist_penetration_testing",
        "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-115.pdf",
    },

    # NIST Digital Identity
    {
        "name": "nist_digital_identity",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-63-4.pdf",
    },

    # NIST Key Management
    {
        "name": "nist_key_management",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-57pt1r5.pdf",
    },

    # NIST Log Management
    {
        "name": "nist_log_management",
        "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-92.pdf",
    },

    # NIST Cloud Security
    {
        "name": "nist_cloud_computing",
        "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-144.pdf",
    },

    # NIST Container Security
    {
        "name": "nist_container_security",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf",
    },

    # Additional NIST security documents
    {
        "name": "nist_idps",
        "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-94.pdf",
    },
    {
        "name": "nist_forensics",
        "url": "https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-86.pdf",
    },
]


def download_document(name: str, url: str) -> bool:
    output_path = RAW_DIR / f"{name}.pdf"

    try:
        print(f"\nDownloading: {name}")
        print(f"URL: {url}")

        request = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0"
            },
        )

        with urlopen(request, timeout=60) as response:
            data = response.read()

        if not data.startswith(b"%PDF"):
            print(f"FAILED: {name} is not a valid PDF")
            return False

        output_path.write_bytes(data)

        print(f"Saved: {output_path}")
        print(f"Size: {len(data) / 1024 / 1024:.2f} MB")

        return True

    except Exception as e:
        print(f"FAILED: {name}")
        print(f"Error: {e}")
        return False


def main():
    success = 0
    failed = 0

    print("=" * 60)
    print("Iyuno Agent Portfolio - Document Downloader")
    print("=" * 60)

    for document in DOCUMENTS:
        if download_document(
            document["name"],
            document["url"],
        ):
            success += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)
    print(f"Total:   {len(DOCUMENTS)}")
    print(f"Success: {success}")
    print(f"Failed:  {failed}")


if __name__ == "__main__":
    main()