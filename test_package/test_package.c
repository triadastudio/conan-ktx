#include "ktx.h"

#include <stdio.h>

int main(int argc, char **argv)
{
    if (argc < 2) {
        fprintf(stderr, "Need at least one argument\n");
        return 1;
    }

    ktxTexture* texture;
    ktx_error_code_e result;
    result = ktxTexture_CreateFromNamedFile(argv[1],
                                            KTX_TEXTURE_CREATE_LOAD_IMAGE_DATA_BIT,
                                            &texture);
    if (result == KTX_SUCCESS) {
        fprintf(stdout, "%s\n", "Success!");
    } else {
        fprintf(stderr, "Failed with code %d\n", result);
        fprintf(stderr, "Check documentation for error codes");
    }

    return 0;
}
