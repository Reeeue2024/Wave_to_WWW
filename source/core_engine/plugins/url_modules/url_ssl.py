# [ URL / Domain Modules ] TLS/SSL 인증서 정보를 바탕으로 탐지

import os
import sys
import ssl
import socket
from urllib.parse import urlparse
from cryptography import x509
from cryptography.hazmat.backends import default_backend
import certifi


class SSLScorer:
    """
    IN : URL (string)
    OUT : 
        - score (float or None) : 위험 점수 (0.0 ~ 1.0)
    """

    def __init__(self, input_url):
        self.input_url = input_url
        self.cert = None

    """
    인증서 기반 위험도 평가 수행
    """
    def scan(self):
        print("Module Start: [SSL Certificate Scoring]")

        self.cert = self._get_cert()
        if not self.cert:
            print("→ Result: Failed to retrieve certificate.")
            print(f"→ Score: 0.00 (0.0: Safe, 1.0: High Risk)")
            print("\nModule End.")
            print(f"[Normal URL] {self.input_url}")
            return 0.0

        # 무료 인증서 또는 신뢰 낮은 CA가 탐지되면 해당 점수 반환
        score = self._score_free_cert() or self._score_untrusted_ca()

        if score == 0.0:
            print(f"[Normal URL] {self.input_url}")
            print(f"→ Score: 0.00 (0.0: Safe, 1.0: High Risk)")
        else:
            print(f"→ Score: {score:.2f} (0.0: Safe, 1.0: High Risk)")

        print("\nModule End.")
        return score

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
            print(f"[ERROR] SSL Certificate fetch failed: {e}")
            return None

    """
    무료 인증서 여부에 따라 위험 점수 부여
    - O  → 점수 1.0 (위험)
    - X → 점수 0.0 (안전)
    """
    def _score_free_cert(self):
        free_cas = ["Let's Encrypt", "ZeroSSL", "Buypass"]
        issuer = self.cert.issuer.rfc4514_string()
        print(f"[Issuer] {issuer}")
        if any(ca in issuer for ca in free_cas):
            print(f"[Detected] Free SSL Certificate: {self.input_url}")
            return 1.0  # Free SSL certificate detected, score 1.0
        return 0.0  # No free SSL certificate, score 0.0

    """
    신뢰 낮은 인증기관(CA) 여부에 따라 위험 점수 부여
    - O  → 점수 1.0 (위험)
    - X → 점수 0.0 (안전)
    """
    def _score_untrusted_ca(self):
        untrusted_cas = ["StartCom", "WoSign", "WoTrus", "TrustAsia", "CNNIC"]
        issuer = self.cert.issuer.rfc4514_string()
        print(f"[Issuer for Untrusted CA Check] {issuer}")  # 추가된 디버깅 출력
        if any(ca in issuer for ca in untrusted_cas):
            print(f"[Detected] Untrusted Certificate Authority: {self.input_url}")
            return 1.0  # Untrusted CA detected, score 1.0
        return 0.0  # No untrusted CA, score 0.0


# Module Main
if __name__ == "__main__":
    # Input : URL
    if len(sys.argv) != 2:
        print("How to Use : python3 url_ssl.py < URL >")
        sys.exit(1)

    # URL 입력 및 점수 평가 실행
    input_url = sys.argv[1]
    scorer = SSLScorer(input_url)
    scorer.scan()  
