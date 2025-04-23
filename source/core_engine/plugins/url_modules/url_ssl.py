# [ URL / Domain Modules ] TLS/SSL

import os
import sys
import ssl
import socket
from urllib.parse import urlparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import certifi


class UrlSsl:
    """
    IN  : input_url (str) - 검사 대상 URL
    OUT : Scan Result
        - True  : Suspicious (무료 인증서 또는 신뢰 낮은 CA 사용)
        - False : Normal (신뢰 가능한 인증서)
        - None  : Unknown (인증서 수집 실패)
    """

    def __init__(self, input_url):
        self.input_url = input_url
        self.cert = None
        self.last_score = None

    """
    인증서 수집
    """
    def _get_cert(self):
        try:
            hostname = urlparse(self.input_url).hostname
            context = ssl.create_default_context(cafile=certifi.where())
            conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
            conn.settimeout(5)
            conn.connect((hostname, 443))
            der_cert = conn.getpeercert(binary_form=True)
            cert = x509.load_der_x509_certificate(der_cert, default_backend())
            return cert
        except Exception as e:
            # print(f"[ERROR] SSL Certificate fetch failed: {e}")
            return False

    """
    무료 인증서 여부에 따라 위험 점수 부여
    """
    def _score_free_cert(self):
        free_cas = [
            "Let's Encrypt", "ZeroSSL", "Buypass",
            "SSL For Free", "FreeSSL", "Basic DV",
            "GeoTrust DV", "cPanel Inc", "Sectigo (DV Only)", "RapidSSL"
        ]
        issuer = self.cert.issuer.rfc4514_string()
        # print(f"[Issuer] {issuer}")
        if any(ca in issuer for ca in free_cas):
            # print(f"[Detected] Free SSL Certificate: {self.input_url}")
            return True
        return False 

    """
    신뢰 낮은 인증기관(CA) 여부에 따라 위험 점수 부여
    """
    def _score_untrusted_ca(self):
        untrusted_cas = [
            "StartCom", "WoSign", "WoTrus", "TrustAsia", "CNNIC",
            "Symantec", "Unizeto", "Comodo", "SwissSign",
            "Certum", "DigiNotar", "PKIoverheid"
        ]
        issuer = self.cert.issuer.rfc4514_string()
        # print(f"[Issuer for Untrusted CA Check] {issuer}")
        if any(ca in issuer for ca in untrusted_cas):
            # print(f"[Detected] Untrusted Certificate Authority: {self.input_url}")
            return 1.0  # Untrusted CA detected, score 1.0
        return 0.0  # No untrusted CA, score 0.0

    def scan(self):
        """
        SSL 인증서 분석을 통한 위험 점수
        - 인증서 없음         → return False (평가 불가, 안전으로 간주)
        - 무료 인증서 사용     → return True  (의심 URL)
        - 신뢰 낮은 CA 사용    → return True  (의심 URL)
        - 그 외 신뢰 인증서    → return False (정상 URL)
        """
        # print("Module Start: [URL TLS/SSL]")

        self.cert = self._get_cert()
        if not self.cert:
            # print("→ Result: Failed to retrieve certificate.")
            # print("→ Score: 0.00 (0.0: Safe, 1.0: High Risk)")
            # print("\nModule End.")
            # print(f"[Normal URL] {self.input_url}")
            self.last_score = 0.0
            return False

        free_score = self._score_free_cert()
        untrusted_score = self._score_untrusted_ca()
        final_score = max(free_score, untrusted_score)
        self.last_score = final_score

        # if final_score == 0.0:
        #     # print(f"[Normal URL] {self.input_url}")
        #     print(f"→ Score: 0.00 (0.0: Safe, 1.0: High Risk)")
        # else:
        #     print(f"→ Score: {final_score:.2f} (0.0: Safe, 1.0: High Risk)")

        # print("\nModule End.")
        return final_score > False


# Module Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        # print("How to Use : python3 url_ssl.py < URL >")
        sys.exit(1)

    # URL 입력 및 점수 평가 실행
    input_url = sys.argv[1]
    url_ssl = UrlSsl(input_url)
    url_ssl.scan()
