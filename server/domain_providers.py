import requests
import json
import time
from typing import Dict, List, Optional, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum


class DNSRecordType(Enum):
    A = "A"
    CNAME = "CNAME"
    TXT = "TXT"
    MX = "MX"
    NS = "NS"


@dataclass
class DNSRecord:
    type: DNSRecordType
    name: str
    value: str
    ttl: int = 3600
    priority: Optional[int] = None


class DomainProvider(ABC):
    """Abstract base class for domain providers"""

    def __init__(self, api_key: str, api_secret: str = None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = self.get_base_url()
        self.headers = self.get_headers()

    @abstractmethod
    def get_base_url(self) -> str:
        """Get the base URL for the provider's API"""
        pass

    @abstractmethod
    def get_headers(self) -> Dict[str, str]:
        """Get headers required for API requests"""
        pass

    @abstractmethod
    def list_domains(self) -> List[Dict[str, Any]]:
        """List all domains in the account"""
        pass

    @abstractmethod
    def list_dns_records(self, domain: str) -> List[DNSRecord]:
        """List DNS records for a domain"""
        pass

    @abstractmethod
    def add_dns_record(self, domain: str, record: DNSRecord) -> Dict[str, Any]:
        """Add a DNS record to a domain"""
        pass

    @abstractmethod
    def update_dns_record(
        self, domain: str, record_id: str, record: DNSRecord
    ) -> Dict[str, Any]:
        """Update an existing DNS record"""
        pass

    @abstractmethod
    def delete_dns_record(self, domain: str, record_id: str) -> bool:
        """Delete a DNS record"""
        pass

    def verify_domain_ownership(self, domain: str) -> bool:
        """Verify that the domain is owned by the account"""
        domains = self.list_domains()
        return any(d["name"] == domain for d in domains)


class GoDaddyProvider(DomainProvider):
    """GoDaddy DNS API integration"""

    def get_base_url(self) -> str:
        return "https://api.godaddy.com/v1"

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"sso-key {self.api_key}:{self.api_secret}",
            "Content-Type": "application/json",
        }

    def list_domains(self) -> List[Dict[str, Any]]:
        """List all domains in GoDaddy account"""
        response = requests.get(f"{self.base_url}/domains", headers=self.headers)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to list domains: {response.text}")

    def list_dns_records(self, domain: str) -> List[DNSRecord]:
        """List DNS records for a domain"""
        response = requests.get(
            f"{self.base_url}/domains/{domain}/records", headers=self.headers
        )

        if response.status_code == 200:
            records = response.json()
            return [
                DNSRecord(
                    type=DNSRecordType(record["type"]),
                    name=record["name"],
                    value=record["data"],
                    ttl=record.get("ttl", 3600),
                )
                for record in records
            ]
        else:
            raise Exception(f"Failed to list DNS records: {response.text}")

    def add_dns_record(self, domain: str, record: DNSRecord) -> Dict[str, Any]:
        """Add a DNS record to a domain"""
        record_data = {
            "type": record.type.value,
            "name": record.name,
            "data": record.value,
            "ttl": record.ttl,
        }

        if record.priority:
            record_data["priority"] = record.priority

        response = requests.put(
            f"{self.base_url}/domains/{domain}/records/{record.name}/{record.type.value}",
            headers=self.headers,
            json=[record_data],
        )

        if response.status_code == 200:
            return {"status": "success", "message": "Record added successfully"}
        else:
            raise Exception(f"Failed to add DNS record: {response.text}")

    def update_dns_record(
        self, domain: str, record_id: str, record: DNSRecord
    ) -> Dict[str, Any]:
        """Update an existing DNS record"""
        return self.add_dns_record(
            domain, record
        )  # GoDaddy uses PUT for both add/update

    def delete_dns_record(self, domain: str, record_id: str) -> bool:
        """Delete a DNS record"""
        response = requests.delete(
            f"{self.base_url}/domains/{domain}/records/{record_id}",
            headers=self.headers,
        )

        return response.status_code == 204


class NamecheapProvider(DomainProvider):
    """Namecheap DNS API integration"""

    def get_base_url(self) -> str:
        return (
            "https://api.sandbox.namecheap.com/xml.response"  # Use sandbox for testing
        )

    def get_headers(self) -> Dict[str, str]:
        return {"Content-Type": "application/xml"}

    def _make_request(self, params: Dict[str, str]) -> Dict[str, Any]:
        """Make API request to Namecheap"""
        params.update(
            {
                "ApiUser": self.api_key,
                "ApiKey": self.api_secret,
                "UserName": self.api_key,
                "ClientIp": "127.0.0.1",  # Required by Namecheap
            }
        )

        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            # Parse XML response (simplified)
            return {"status": "success", "data": response.text}
        else:
            raise Exception(f"Namecheap API request failed: {response.text}")

    def list_domains(self) -> List[Dict[str, Any]]:
        """List all domains in Namecheap account"""
        params = {"Command": "namecheap.domains.getList"}
        result = self._make_request(params)

        # Parse XML response to extract domains
        # This is a simplified implementation
        return [{"name": "example.com"}]  # Placeholder

    def list_dns_records(self, domain: str) -> List[DNSRecord]:
        """List DNS records for a domain"""
        params = {
            "Command": "namecheap.domains.dns.getHosts",
            "SLD": domain.split(".")[0],
            "TLD": domain.split(".")[1],
        }

        result = self._make_request(params)
        # Parse XML response to extract records
        return []  # Placeholder

    def add_dns_record(self, domain: str, record: DNSRecord) -> Dict[str, Any]:
        """Add a DNS record to a domain"""
        params = {
            "Command": "namecheap.domains.dns.setHosts",
            "SLD": domain.split(".")[0],
            "TLD": domain.split(".")[1],
            "HostName": record.name,
            "RecordType": record.type.value,
            "Address": record.value,
            "TTL": str(record.ttl),
        }

        return self._make_request(params)

    def update_dns_record(
        self, domain: str, record_id: str, record: DNSRecord
    ) -> Dict[str, Any]:
        """Update an existing DNS record"""
        return self.add_dns_record(domain, record)

    def delete_dns_record(self, domain: str, record_id: str) -> bool:
        """Delete a DNS record"""
        # Namecheap requires setting all records, so we'd need to get current records
        # and set them without the one to delete
        return True


class CloudflareProvider(DomainProvider):
    """Cloudflare DNS API integration"""

    def get_base_url(self) -> str:
        return "https://api.cloudflare.com/client/v4"

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def list_domains(self) -> List[Dict[str, Any]]:
        """List all domains in Cloudflare account"""
        response = requests.get(f"{self.base_url}/zones", headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            return data.get("result", [])
        else:
            raise Exception(f"Failed to list domains: {response.text}")

    def get_zone_id(self, domain: str) -> str:
        """Get zone ID for a domain"""
        zones = self.list_domains()
        for zone in zones:
            if zone["name"] == domain:
                return zone["id"]
        raise Exception(f"Domain {domain} not found in Cloudflare account")

    def list_dns_records(self, domain: str) -> List[DNSRecord]:
        """List DNS records for a domain"""
        zone_id = self.get_zone_id(domain)
        response = requests.get(
            f"{self.base_url}/zones/{zone_id}/dns_records", headers=self.headers
        )

        if response.status_code == 200:
            data = response.json()
            records = data.get("result", [])
            return [
                DNSRecord(
                    type=DNSRecordType(record["type"]),
                    name=record["name"],
                    value=record["content"],
                    ttl=record.get("ttl", 3600),
                )
                for record in records
            ]
        else:
            raise Exception(f"Failed to list DNS records: {response.text}")

    def add_dns_record(self, domain: str, record: DNSRecord) -> Dict[str, Any]:
        """Add a DNS record to a domain"""
        zone_id = self.get_zone_id(domain)

        record_data = {
            "type": record.type.value,
            "name": record.name,
            "content": record.value,
            "ttl": record.ttl,
        }

        if record.priority:
            record_data["priority"] = record.priority

        response = requests.post(
            f"{self.base_url}/zones/{zone_id}/dns_records",
            headers=self.headers,
            json=record_data,
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to add DNS record: {response.text}")

    def update_dns_record(
        self, domain: str, record_id: str, record: DNSRecord
    ) -> Dict[str, Any]:
        """Update an existing DNS record"""
        zone_id = self.get_zone_id(domain)

        record_data = {
            "type": record.type.value,
            "name": record.name,
            "content": record.value,
            "ttl": record.ttl,
        }

        if record.priority:
            record_data["priority"] = record.priority

        response = requests.put(
            f"{self.base_url}/zones/{zone_id}/dns_records/{record_id}",
            headers=self.headers,
            json=record_data,
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update DNS record: {response.text}")

    def delete_dns_record(self, domain: str, record_id: str) -> bool:
        """Delete a DNS record"""
        zone_id = self.get_zone_id(domain)
        response = requests.delete(
            f"{self.base_url}/zones/{zone_id}/dns_records/{record_id}",
            headers=self.headers,
        )

        return response.status_code == 200


class SquarespaceProvider(DomainProvider):
    """Squarespace DNS API integration"""

    def get_base_url(self) -> str:
        return "https://api.squarespace.com/1.0"

    def get_headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def list_domains(self) -> List[Dict[str, Any]]:
        """List all domains in Squarespace account"""
        response = requests.get(f"{self.base_url}/domains", headers=self.headers)

        if response.status_code == 200:
            return response.json().get("domains", [])
        else:
            raise Exception(f"Failed to list domains: {response.text}")

    def list_dns_records(self, domain: str) -> List[DNSRecord]:
        """List DNS records for a domain"""
        response = requests.get(
            f"{self.base_url}/domains/{domain}/dns", headers=self.headers
        )

        if response.status_code == 200:
            records = response.json().get("records", [])
            return [
                DNSRecord(
                    type=DNSRecordType(record["type"]),
                    name=record["name"],
                    value=record["data"],
                    ttl=record.get("ttl", 3600),
                )
                for record in records
            ]
        else:
            raise Exception(f"Failed to list DNS records: {response.text}")

    def add_dns_record(self, domain: str, record: DNSRecord) -> Dict[str, Any]:
        """Add a DNS record to a domain"""
        record_data = {
            "type": record.type.value,
            "name": record.name,
            "data": record.value,
            "ttl": record.ttl,
        }

        if record.priority:
            record_data["priority"] = record.priority

        response = requests.post(
            f"{self.base_url}/domains/{domain}/dns",
            headers=self.headers,
            json=record_data,
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to add DNS record: {response.text}")

    def update_dns_record(
        self, domain: str, record_id: str, record: DNSRecord
    ) -> Dict[str, Any]:
        """Update an existing DNS record"""
        record_data = {
            "type": record.type.value,
            "name": record.name,
            "data": record.value,
            "ttl": record.ttl,
        }

        if record.priority:
            record_data["priority"] = record.priority

        response = requests.put(
            f"{self.base_url}/domains/{domain}/dns/{record_id}",
            headers=self.headers,
            json=record_data,
        )

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to update DNS record: {response.text}")

    def delete_dns_record(self, domain: str, record_id: str) -> bool:
        """Delete a DNS record"""
        response = requests.delete(
            f"{self.base_url}/domains/{domain}/dns/{record_id}", headers=self.headers
        )

        return response.status_code == 204


class DomainManager:
    """High-level domain management interface"""

    def __init__(self):
        self.providers = {}

    def register_provider(self, name: str, provider: DomainProvider):
        """Register a domain provider"""
        self.providers[name] = provider

    def get_provider(self, name: str) -> DomainProvider:
        """Get a registered provider"""
        if name not in self.providers:
            raise Exception(f"Provider '{name}' not registered")
        return self.providers[name]

    def setup_render_domains(
        self, provider_name: str, domain: str, render_service_url: str
    ) -> Dict[str, Any]:
        """Set up DNS records for Render deployment"""
        provider = self.get_provider(provider_name)

        # Verify domain ownership
        if not provider.verify_domain_ownership(domain):
            raise Exception(f"Domain {domain} not found in {provider_name} account")

        # Create CNAME record for Render service
        cname_record = DNSRecord(
            type=DNSRecordType.CNAME,
            name="@",  # Root domain
            value=render_service_url,
            ttl=3600,
        )

        try:
            # Add the CNAME record
            result = provider.add_dns_record(domain, cname_record)

            return {
                "status": "success",
                "message": f"DNS record added for {domain}",
                "provider": provider_name,
                "record": cname_record.__dict__,
                "result": result,
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Failed to add DNS record: {str(e)}",
                "provider": provider_name,
            }

    def setup_fullstack_domains(
        self,
        provider_name: str,
        frontend_domain: str,
        backend_domain: str,
        frontend_url: str,
        backend_url: str,
    ) -> Dict[str, Any]:
        """Set up DNS records for full-stack application"""
        provider = self.get_provider(provider_name)

        results = {}

        # Set up frontend domain
        if frontend_domain:
            frontend_record = DNSRecord(
                type=DNSRecordType.CNAME, name="@", value=frontend_url, ttl=3600
            )

            try:
                results["frontend"] = provider.add_dns_record(
                    frontend_domain, frontend_record
                )
            except Exception as e:
                results["frontend"] = {"error": str(e)}

        # Set up backend domain
        if backend_domain:
            backend_record = DNSRecord(
                type=DNSRecordType.CNAME,
                name="api" if backend_domain.startswith("api.") else "@",
                value=backend_url,
                ttl=3600,
            )

            try:
                results["backend"] = provider.add_dns_record(
                    backend_domain, backend_record
                )
            except Exception as e:
                results["backend"] = {"error": str(e)}

        return {
            "status": "success",
            "message": "DNS records configured for full-stack application",
            "provider": provider_name,
            "results": results,
        }

    def list_provider_domains(self, provider_name: str) -> List[Dict[str, Any]]:
        """List all domains for a provider"""
        provider = self.get_provider(provider_name)
        return provider.list_domains()

    def get_domain_records(self, provider_name: str, domain: str) -> List[DNSRecord]:
        """Get DNS records for a domain"""
        provider = self.get_provider(provider_name)
        return provider.list_dns_records(domain)

    def verify_dns_propagation(
        self, domain: str, expected_value: str, record_type: str = "CNAME"
    ) -> bool:
        """Verify DNS propagation using external DNS lookup"""
        import dns.resolver

        try:
            answers = dns.resolver.resolve(domain, record_type)
            for answer in answers:
                if str(answer) == expected_value:
                    return True
            return False
        except Exception:
            return False


# Provider factory
def create_provider(
    provider_type: str, api_key: str, api_secret: str = None
) -> DomainProvider:
    """Create a domain provider instance"""

    providers = {
        "godaddy": GoDaddyProvider,
        "namecheap": NamecheapProvider,
        "cloudflare": CloudflareProvider,
        "squarespace": SquarespaceProvider,
    }

    if provider_type.lower() not in providers:
        raise Exception(f"Unsupported provider: {provider_type}")

    return providers[provider_type.lower()](api_key, api_secret)
