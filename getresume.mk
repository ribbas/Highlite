# Extra rules for installing getresume and configuring Tor and Privoxy
SECRET="getresume/getresume/settings/secret"
TARFILE="getresume.tar.gz"

.PHONY: getresume
getresume:
	# clone and install getresume
	@git clone https://github.com/sabbirahm3d/getresume
	@mv getresume/dist/getresume-* ${TARFILE}
	@rm -rf getresume
	@tar -xvf ${TARFILE}
	@mv getresume-* getresume
	@echo -n ${PASSWORD} > ${SECRET}
	@python getresume/setup.py install

	# hash password and append it to torrc
	@ln -s /etc/tor/torrc torrc
	@ln -s /etc/privoxy/config privoxyconfig
	@sudo bash -c 'echo "ControlPort 9051" >> torrc'
	@sudo bash -c 'echo -n "HashedControlPassword " >> torrc'
	@sudo bash -c 'echo -n "$(shell tor --hash-password ${PASSWORD})" >> torrc'
	@sudo bash -c 'echo "forward-socks5 / localhost:9050" >> privoxyconfig'

	# clean up
	@find . -path "./getresume*" ! -name "getresume.mk" -type f -delete
	@find . \( -path "./build/*" -o -path "./dist/*"  \) -delete
	@find . \( -path "./build" -o -path "./dist" \) -empty -delete
