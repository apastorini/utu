import pathlib

CLASES = pathlib.Path(r'C:\Utu\utu\redescomp\clases')

FIX = {
    'clase-13-correo.md': [
        ('Es la clave del formato .',
         'Es la clave del formato MIME.'),
        ('> el cliente manda **. Si la conexión se cae antes del , los mensajes marcados',
         '> el cliente manda `QUIT`. Si la conexión se cae antes del `QUIT`, los mensajes marcados'),
        ('éxito y  es error.** Todos los comandos empiezan por  o , y',
         'éxito y `-ERR` es error.** Todos los comandos empiezan por `+OK` o `-ERR`, y'),
        ('3. ** dice , pero todavía no se borró.** Se borró en el .',
         '3. **`DELE` dice `+OK`, pero todavía no se borró.** Se borró en el `QUIT`.'),
        ('solo borra en el .',
         'solo borra en el `QUIT`.'),
        ('terminar en ; los puertos **465**, **993** y **995** son de TLS implí',
         'terminar en `QUIT`; los puertos **465**, **993** y **995** son de TLS implícito'),
        ('acentos, así que el texto va en ; el PDF es binario y va en .',
         'acentos, así que el texto va en `quoted-printable`; el PDF es binario y va en `base64`.'),
        (',  y . Tiene una notebook y un celular, y los dos se conectan',
         ', `nuevo@lugar.com` y `Viejo@lugar.com`. Tiene una notebook y un celular, y los dos se conectan'),
    ],
}


def main():
    for nombre, items in FIX.items():
        p = CLASES / nombre
        t = p.read_text(encoding='utf-8')
        ok = 0
        for viejo, nuevo in items:
            if viejo in t:
                t = t.replace(viejo, nuevo, 1)
                ok += 1
            else:
                print(f"  NO ENCONTRADO: {viejo[:70]}")
        p.write_text(t, encoding='utf-8', newline='\n')
        print(f"{nombre}: {ok}/{len(items)}")


if __name__ == '__main__':
    main()
