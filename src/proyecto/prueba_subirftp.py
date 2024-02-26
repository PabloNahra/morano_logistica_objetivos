import funciones_generales

# Ejemplo de uso
servidor_ftp = '54.245.133.116'
usuario_ftp = 'sftp-user'
pass_ftp = 'L1EtoN90JKuLkSow'
archivo_local = 'archivo_local.csv'
archivo_remoto = '/sftp/prod/orderStatus/toProcess/archivo_local.csv'

funciones_generales.subir_archivo_ftp(servidor_ftp, usuario_ftp, pass_ftp, archivo_local, archivo_remoto)
