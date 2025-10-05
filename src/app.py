print("Simulating build process...")
print("Compiling project...")

# Intentional failure
raise Exception("Build failed due to missing dependency: requests module not found")
