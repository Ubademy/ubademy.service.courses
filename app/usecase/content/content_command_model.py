from pydantic import BaseModel, Field


class ContentCreateModel(BaseModel):

    title: str = Field(example="FFT: Fast Fourier Transform")
    chapter: int = Field(ge=0, example=1)
    order: int = Field(ge=0, example=0)
    description: str = Field(
        example="A fast Fourier transform (FFT) is an algorithm that computes the discrete Fourier transform (DFT) of "
        "a sequence, or its inverse (IDFT). Fourier analysis converts a signal from its original domain ("
        "often time or space) to a representation in the frequency domain and vice versa. The DFT is obtained "
        "by decomposing a sequence of values into components of different frequencies. "
    )
    video: str = Field(
        default="", example="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    image: str = Field(
        default="",
        example="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
    )


class ContentUpdateModel(BaseModel):

    title: str = Field(default=None, example="FFT: Fast Fourier Transform")
    chapter: int = Field(default=None, ge=0, example=1)
    order: int = Field(default=None, ge=0, example=0)
    description: str = Field(
        default=None,
        example="A fast Fourier transform (FFT) is an algorithm that computes the discrete Fourier transform (DFT) of "
        "a sequence, or its inverse (IDFT). Fourier analysis converts a signal from its original domain ("
        "often time or space) to a representation in the frequency domain and vice versa. The DFT is obtained "
        "by decomposing a sequence of values into components of different frequencies. ",
    )
    video: str = Field(
        default=None, example="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    )
    image: str = Field(
        default=None,
        example="https://static01.nyt.com/images/2017/09/26/science/26TB-PANDA/26TB-PANDA-superJumbo.jpg",
    )
    active: bool = Field(default=None, example=True)
