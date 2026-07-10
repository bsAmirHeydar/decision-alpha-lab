# Rollback and Cleanup

Rollback consists of removing the P09 Expert and SessionBox include files. Existing objects may be deleted with the P09 prefix cleanup function or by enabling deinit cleanup for a controlled run.

Never use global object deletion. P08 trend lines and all foreign drawings must survive rollback.
