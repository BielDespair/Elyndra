from enum import Enum

class Region(str, Enum):
    BR = "BR"
    JP = "JP"
    KR = "KR"
    
    
    
class TipoPreco(str, Enum):
    GRATIS = "GRATIS"
    PAGO = "PAGO"
    ASSINATURA = "ASSINATURA"
    
class Moeda(str, Enum):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"
    
    
    
class Idioma(str, Enum):
    PT_BR = "pt-BR"
    PT_PT = "pt-PT"
    EN_US = "en-US"
    EN_GB = "en-GB"
    ES_ES = "es-ES"
    ES_MX = "es-MX"
    FR_FR = "fr-FR"
    DE_DE = "de-DE"
    IT_IT = "it-IT"
    RU_RU = "ru-RU"
    ZH_CN = "zh-CN"
    ZH_TW = "zh-TW" 
    JA_JP = "ja-JP"
    KO_KR = "ko-KR"
    PL_PL = "pl-PL"
    TR_TR = "tr-TR"
    NL_NL = "nl-NL"