from manifest import generate_manifest, check_integrity
from signer import generate_keys, sign_file, verify_signature
print("1. Generate metadata")
print("2. Check integrity")
print("3. Generate RSA keys")
print("4. Sign metadata")
print("5. Verify signature")

choice = input("Choose option: ")

if choice == "1":
    generate_manifest("data")

elif choice == "2":
    check_integrity("data")

elif choice == "3":
    generate_keys()

elif choice == "4":
    sign_file()

elif choice == "5":
    verify_signature()

else:
    print("Invalid choice")