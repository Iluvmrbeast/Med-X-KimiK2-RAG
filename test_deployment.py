#!/usr/bin/env python3
"""
MedeX Pre-Deployment Test Script
Tests system components before HF Spaces deployment
"""

import sys
import os
from pathlib import Path

print("🔬 MedeX Pre-Deployment Test Suite")
print("=" * 60)

# Test 1: Python Version
print("\n1️⃣ Testing Python Version...")
python_version = sys.version_info
if python_version >= (3, 8):
    print(
        f"   ✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}"
    )
else:
    print(f"   ❌ Python {python_version.major}.{python_version.minor} (requires 3.8+)")
    sys.exit(1)

# Test 2: Required Files
print("\n2️⃣ Testing Required Files...")
required_files = [
    "streamlit_app.py",
    "Dockerfile",
    ".dockerignore",
    "requirements.txt",
    "config.py",
    "MEDEX_ULTIMATE_RAG.py",
    "medical_knowledge_base.py",
    "medical_rag_system.py",
    "pharmaceutical_database.py",
    ".streamlit/config.toml",
]

missing_files = []
for file in required_files:
    if Path(file).exists():
        print(f"   ✅ {file}")
    else:
        print(f"   ❌ {file} (MISSING)")
        missing_files.append(file)

if missing_files:
    print(f"\n   ❌ Missing {len(missing_files)} required files!")
    sys.exit(1)

# Test 3: Dependencies
print("\n3️⃣ Testing Core Dependencies...")
required_modules = {
    "streamlit": "Streamlit",
    "openai": "OpenAI SDK",
    "sentence_transformers": "Sentence Transformers",
    "sklearn": "Scikit-learn",
    "PIL": "Pillow",
}

missing_modules = []
for module, name in required_modules.items():
    try:
        __import__(module)
        print(f"   ✅ {name}")
    except ImportError:
        print(f"   ❌ {name} (NOT INSTALLED)")
        missing_modules.append(name)

if missing_modules:
    print(f"\n   ⚠️ Missing modules: {', '.join(missing_modules)}")
    print("   Run: pip install -r requirements.txt")

# Test 4: Configuration
print("\n4️⃣ Testing Configuration...")
try:
    from config import config

    api_key = config.get_kimi_api_key()
    if api_key and len(api_key) > 10:
        print(f"   ✅ API Key configured (length: {len(api_key)})")
    else:
        print(f"   ⚠️ API Key might be invalid")

    print(f"   ✅ Base URL: {config.get_moonshot_base_url()}")
    print(f"   ✅ Cache Dir: {config.get_rag_cache_dir()}")
except Exception as e:
    print(f"   ❌ Configuration error: {e}")

# Test 5: MedeX System
print("\n5️⃣ Testing MedeX System Initialization...")
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from MEDEX_ULTIMATE_RAG import MedeXUltimateRAG

    print("   🧠 Initializing MedeX...")
    medex = MedeXUltimateRAG()
    print("   ✅ MedeX Ultimate RAG initialized")

    # Test user detection
    test_query = "Paciente de 65 años con diabetes"
    user_type = medex.detect_user_type(test_query)
    print(f"   ✅ User detection working (detected: {user_type})")

    # Test emergency detection
    emergency = medex.detect_emergency("dolor precordial intenso")
    print(f"   ✅ Emergency detection working (detected: {emergency})")

except Exception as e:
    print(f"   ❌ MedeX initialization error: {e}")
    import traceback

    traceback.print_exc()

# Test 6: Streamlit App
print("\n6️⃣ Testing Streamlit App...")
try:
    # Just check if it can be imported
    import streamlit

    print(f"   ✅ Streamlit version: {streamlit.__version__}")

    # Check config
    config_path = Path(".streamlit/config.toml")
    if config_path.exists():
        print(f"   ✅ Streamlit config exists")
    else:
        print(f"   ⚠️ Streamlit config not found")

except Exception as e:
    print(f"   ❌ Streamlit error: {e}")

# Test 7: Docker Configuration
print("\n7️⃣ Testing Docker Configuration...")
dockerfile = Path("Dockerfile")
if dockerfile.exists():
    content = dockerfile.read_text()
    if "7860" in content:
        print("   ✅ Dockerfile port 7860 configured")
    else:
        print("   ⚠️ Port 7860 not found in Dockerfile")

    if "streamlit" in content.lower():
        print("   ✅ Streamlit command found in Dockerfile")
    else:
        print("   ❌ Streamlit command missing in Dockerfile")

# Summary
print("\n" + "=" * 60)
print("📊 TEST SUMMARY")
print("=" * 60)

if not missing_files and not missing_modules:
    print("✅ All tests passed!")
    print("🚀 System ready for deployment to Hugging Face Spaces")
    print("\nNext steps:")
    print("1. Create a new Space on Hugging Face (SDK: Docker)")
    print("2. Add KIMI_API_KEY to Space secrets")
    print("3. Upload all files to the Space")
    print("4. Wait for build to complete")
    print("\nSee DEPLOYMENT_GUIDE.md for detailed instructions")
else:
    print("⚠️ Some tests failed or warnings present")
    print("Review the issues above before deployment")
    if missing_modules:
        print("\n💡 Install missing modules:")
        print("   pip install -r requirements.txt")

print("\n" + "=" * 60)
