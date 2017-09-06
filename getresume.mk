# Extra rules for installing getresume and configuring Tor and Privoxy
SECRET="secret"

.PHONY: getresume
getresume:
	# hash password and append it to torrc
	@git clone https://github.com/sabbirahm3d/getresume
	@mv dist/* .
	@tar -xvf getresume*
	@python 
	@echo -n ${PASSWORD} > ${SECRET}
	# @ln -s /etc/tor/torrc torrc
	# @ln -s /etc/privoxy/config privoxyconfig
	# @sudo bash -c 'echo "ControlPort 9051" >> torrc'
	# @sudo bash -c 'echo -n "HashedControlPassword " >> torrc'
	# @sudo bash -c 'echo -n "$(shell tor --hash-password ${PASSWORD})" >> torrc'
	# @sudo bash -c 'echo "forward-socks5 / localhost:9050" >> privoxyconfig'
