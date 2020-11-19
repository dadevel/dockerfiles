FROM archlinux:latest
ENV TERM xterm
ENV USER_ID 1000
ENV GROUP_ID 1000
COPY ./pacman.conf /etc/pacman.conf
COPY ./sudoers /etc/sudoers
RUN pacman --sync --refresh --sysupgrade --noconfirm sudo && \
find / -type f '(' -name '*.pacnew' -or -name '*.pacsave' ')' -delete 2> /dev/null && \
chmod 440 /etc/sudoers && \
groupadd --gid $GROUP_ID penelope && \
useradd --uid $USER_ID --gid $GROUP_ID --groups wheel --create-home penelope
RUN curl --silent --show-error https://blackarch.org/strap.sh | bash
COPY ./entrypoint.sh /
WORKDIR /home/penelope
ENTRYPOINT ["/entrypoint.sh"]
CMD ["bash", "-i"]

