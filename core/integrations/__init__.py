"""
Système d'intégrations pour les agents spécialisés
"""

from .base import BaseIntegration, IntegrationStatus
from .social_media import InstagramIntegration, TwitterIntegration, LinkedInIntegration, FacebookIntegration, TikTokIntegration
from .customer_support import ZendeskIntegration, IntercomIntegration, FreshdeskIntegration
from .seo import GoogleSearchConsoleIntegration, SEMrushIntegration, AhrefsIntegration
from .analytics import GoogleAnalyticsIntegration, MixpanelIntegration, AmplitudeIntegration
from .crm import SalesforceIntegration, HubSpotIntegration, PipedriveIntegration
from .email import MailchimpIntegration, SendGridIntegration, BrevoIntegration
from .content import GrammarlyIntegration, CopyAIIntegration, JasperIntegration

__all__ = [
    'BaseIntegration',
    'IntegrationStatus',
    # Social Media
    'InstagramIntegration',
    'TwitterIntegration',
    'LinkedInIntegration',
    'FacebookIntegration',
    'TikTokIntegration',
    # Customer Support
    'ZendeskIntegration',
    'IntercomIntegration',
    'FreshdeskIntegration',
    # SEO
    'GoogleSearchConsoleIntegration',
    'SEMrushIntegration',
    'AhrefsIntegration',
    # Analytics
    'GoogleAnalyticsIntegration',
    'MixpanelIntegration',
    'AmplitudeIntegration',
    # CRM
    'SalesforceIntegration',
    'HubSpotIntegration',
    'PipedriveIntegration',
    # Email
    'MailchimpIntegration',
    'SendGridIntegration',
    'BrevoIntegration',
    # Content
    'GrammarlyIntegration',
    'CopyAIIntegration',
    'JasperIntegration',
]

