import re
from urllib.parse import urlparse

class FeatureExtraction:
    def __init__(self, url):
        self.url = url.lower()
        self.parsed = urlparse(url)
        self.domain = self.parsed.netloc

    def has_ip(self):
        return -1 if re.match(r"\d+\.\d+\.\d+\.\d+", self.url) else 1

    def url_length(self):
        return 1 if len(self.url) < 60 else -1

    def has_at_symbol(self):
        return -1 if "@" in self.url else 1

    def has_prefix_suffix(self):
        return -1 if "-" in self.domain else 1

    def subdomain_count(self):
        return self.domain.count(".")

    def is_https(self):
        return 1 if self.parsed.scheme == "https" else -1

    def has_suspicious_words(self):
        return -1 if re.search(r"login|verify|bank|secure|account|update", self.url) else 1

    def has_long_domain(self):
        return -1 if len(self.domain) > 25 else 1

    def getFeaturesList(self):
        features = [
            self.has_ip(),
            self.url_length(),
            self.has_at_symbol(),
            self.has_prefix_suffix(),
            self.subdomain_count(),
            self.is_https(),
            self.has_suspicious_words(),
            self.has_long_domain(),
        ]

        # 🔥 FIX: FIXED LENGTH ALWAYS SAME
        features = features + [0] * (30 - len(features))

        return [int(x) for x in features]