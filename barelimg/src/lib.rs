use pyo3::{prelude::*, types::PyBytes, ffi::PyCodec_StreamReader};
use std::{io::Cursor, path::Path, fs::File, f64::consts::E};
use image::{ImageFormat, DynamicImage, Rgba, GenericImageView};
use imageproc::{drawing::draw_text, drawing::text_size};
use rusttype::{Font, Scale};
use std::io::Read;
use lazy_static::lazy_static;
use std::sync::Arc;


lazy_static! {
    static ref FONT: Font<'static> = load_font();
}
lazy_static! {
    static ref TEMPLATE_IMG: Arc<DynamicImage> = Arc::new(load_image_f());
}
static COLOR: Rgba<u8> = Rgba([255, 255, 255, 255]);
const FONT_SIZE: f32 = 35f32;
static SCALE: Scale = Scale{x: FONT_SIZE, y: FONT_SIZE};


fn load_image_f() -> DynamicImage {
    println!("loadimagef");
    if let Ok(image) = image::io::Reader::open("template.png").unwrap().decode() {
        return image;
    }
    DynamicImage::default()
}

fn load_image(img: Vec<u8>) -> DynamicImage {
    if let Ok(image) = image::load_from_memory(&img) {
        return image;
    }
    DynamicImage::default()
}


fn calculate_position(text: &str) -> i32 {
    // w595
    let ts = text_size(SCALE, &FONT, text).0;
    let pos = (595 - ts) / 2;
    pos
}

fn load_font() -> Font<'static> {
    println!("loadfont");
    let font_path = Path::new("./font.ttf");
    let mut font_data: Vec<u8> = Vec::new();
    File::open(font_path).unwrap().read_to_end(&mut font_data).unwrap();
    Font::try_from_vec(font_data).unwrap()
}

#[pyfunction]
fn draw_on(text: &str) -> PyResult<PyBytes> {  // img: Vec<u8>, 
    //let mut image = load_image(img);
    //let text_str = text.as_str();
    let drewn = draw_text(
        TEMPLATE_IMG.as_ref(),  // TEMPLATE_IMG: Arc<DynamicImage>
        COLOR,
        calculate_position(text),
        620,
        SCALE,
        &FONT,
        text
    );
    let mut pngbuf: Cursor<Vec<u8>> = Cursor::new(Vec::new());
    drewn.write_to(&mut pngbuf, ImageFormat::Png).unwrap();
    Python::with_gil(|py| {
        Ok(*PyBytes::new(py, &pngbuf.into_inner()))
    })
}

/// A Python module implemented in Rust.
#[pymodule]
fn barelimg(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(draw_on, m)?)?;
    Ok(())
}