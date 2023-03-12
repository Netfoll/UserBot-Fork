#!/bin/bash


runin() {
	# Runs the arguments, piping stderr to logfile
	{ "$@" 2>>../netfoll-install.log || return $?; } | while read -r line; do
		printf "%s\n" "$line" >>../netfoll-install.log
	done
}

runout() {
	# Runs the arguments, piping stderr to logfile
	{ "$@" 2>>netfoll-install.log || return $?; } | while read -r line; do
		printf "%s\n" "$line" >>netfoll-install.log
	done
}

errorin() {
	cat ../netfoll-install.log
}

errorout() {
	cat netfoll-install.log
}

SUDO_CMD=""
if [ ! x"$SUDO_USER" = x"" ]; then
	if command -v sudo >/dev/null; then
		SUDO_CMD="sudo -u $SUDO_USER "
	fi
fi

##############################################################################

clear
clear

printf "\n\e[1;35;47m                   \e[0m"
printf "\n\e[1;35;47m  _   _      _    __       _ _  \e[0m"
printf "\n\e[1;35;47m | \ | | ___| |_ / _| ___ | | | \e[0m"
printf "\n\e[1;35;47m |  \| |/ _ \ __| |_ / _ \| | | \e[0m"
printf "\n\e[1;35;47m | |\  |  __/ |_|  _| (_) | | | \e[0m"
printf "\n\e[1;35;47m |_| \_|\___|\__|_|  \___/|_|_| \e[0m"
printf "\n\e[1;35;47m                                \e[0m"
printf "\n\e[3;34;40m Установка. Пожалуйста, подождите...\e[0m\n\n"

##############################################################################

printf "\r\033[0;34mПопытка установки...\e[0m"

touch netfoll-install.log
if [ ! x"$SUDO_USER" = x"" ]; then
	chown "$SUDO_USER:" netfoll-install.log
fi

if [ -d "Netfoll/netfoll" ]; then
	cd netfoll || {
		printf "\rОшибка: установите гит прежде чем продолжить (pkg/apt install git)"
		exit 6
	}
	DIR_CHANGED="yes"
fi
if [ -f ".setup_complete" ]; then
	# If Netfoll is already installed by this script
	PYVER=""
	if echo "$OSTYPE" | grep -qE '^linux-gnu.*'; then
		PYVER="3"
	fi
	printf "\rExisting installation detected"
	clear
	"python$PYVER" -m netfoll "$@"
	exit $?
elif [ "$DIR_CHANGED" = "yes" ]; then
	cd ..
fi

##############################################################################

echo "Установка..." >netfoll-install.log

if echo "$OSTYPE" | grep -qE '^linux-gnu.*' && [ -f '/etc/debian_version' ]; then
	PKGMGR="apt install -y"
	runout dpkg --configure -a
	runout apt update
	PYVER="3"
elif echo "$OSTYPE" | grep -qE '^linux-gnu.*' && [ -f '/etc/arch-release' ]; then
	PKGMGR="pacman -Sy --noconfirm"
	PYVER="3"
elif echo "$OSTYPE" | grep -qE '^linux-android.*'; then
	runout apt update
	PKGMGR="apt install -y"
	PYVER=""
elif echo "$OSTYPE" | grep -qE '^darwin.*'; then
	if ! command -v brew >/dev/null; then
		ruby <(curl -fsSk https://raw.github.com/mxcl/homebrew/go)
	fi
	PKGMGR="brew install"
	PYVER="3"
else
	printf "\r\033[1;31mНеизвестная OS.\e[0m Пожалуйста прочтите 'Manual installation' at \033[0;94mhttps://github.com/hikariatama/Hikka/#-installation\e[0m"
	exit 1
fi

##############################################################################

runout "$SUDO_CMD $PKGMGR python$PYVER" git || {
	errorout "Ошибка установки ядра."
	exit 2
}


printf "\r\033[K\033[0;32mПодготовка выполнена!\e[0m"
printf "\n\r\033[0;34mУстановка дополнений linux...\e[0m"

if echo "$OSTYPE" | grep -qE '^linux-gnu.*'; then
	runout "$SUDO_CMD $PKGMGR python$PYVER-dev"
	runout "$SUDO_CMD $PKGMGR python$PYVER-pip"
	runout "$SUDO_CMD $PKGMGR python3 python3-pip git python3-dev \
		libwebp-dev libz-dev libjpeg-dev libopenjp2-7 libtiff5 \
		ffmpeg imamgemagick libffi-dev libcairo2"
elif echo "$OSTYPE" | grep -qE '^linux-android.*'; then
	runout "$SUDO_CMD $PKGMGR openssl libjpeg-turbo libwebp libffi libcairo build-essential libxslt libiconv git ncurses-utils"
elif echo "$OSTYPE" | grep -qE '^darwin.*'; then
	runout "$SUDO_CMD$ $PKGMGR jpeg webp"
fi

runout "$SUDO_CMD $PKGMGR neofetch dialog"

printf "\r\033[K\033[0;32mPackages installed!\e[0m"
printf "\n\r\033[0;34mCloning repo...\e[0m"


##############################################################################

# shellcheck disable=SC2086
${SUDO_CMD}rm -rf Netfoll
# shellcheck disable=SC2086
runout ${SUDO_CMD}git clone https://github.com/MXRRI/Netfoll || {
	errorout "Ошибка клонирования."
	exit 3
}
cd Netfoll || {
	printf "\r\033[0;33mВведи: \033[1;33mpkg install git\033[0;33m и повтори установку."
	exit 7
}

printf "\r\033[K\033[0;32mРепо клонирован!\e[0m"
printf "\n\r\033[0;34mУстановка необходимых компонентов...\e[0m"

# shellcheck disable=SC2086
runin "$SUDO_CMD python$PYVER" -m pip install --upgrade pip setuptools wheel --user
# shellcheck disable=SC2086
runin "$SUDO_CMD python$PYVER" -m pip install -r requirements.txt --upgrade --user --no-warn-script-location --disable-pip-version-check || {
	errorin "Ошибка зависимостей!"
	exit 4
}
rm -f ../netfoll-install.log
touch .setup_complete

printf "\r\033[K\033[0;32mDependencies installed!\e[0m"
printf "\n\033[0;32mДобро пожаловать...\e[0m\n\n"

${SUDO_CMD}"python$PYVER" -m netfoll "$@" || {
	printf "\033[1;31mPython scripts failed\e[0m"
	exit 5
}
