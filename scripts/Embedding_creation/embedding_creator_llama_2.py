from transformers import AutoModel, AutoTokenizer
from sklearn.metrics.pairwise import cosine_similarity

model = AutoModel.from_pretrained('mesolitica/llama2-embedding-1b-8k', trust_remote_code = True)
tokenizer = AutoTokenizer.from_pretrained('mesolitica/llama2-embedding-1b-8k')


input_ids = tokenizer(
    [
        'schreibt, hat mehr als ein narzisstisches Anliegen. Im eigenen Erleben spiegeln sich', 
        'Isu perkauman: Kerajaan didakwa terdesak kaitkan pemimpin PN',
        'nasi ayam tu sedap', 
        'suka ikan goreng?',
        'Kerajaan tidak akan berkompromi dengan isu perkauman dan agama yang dimanipulasi pihak tertentu untuk mengganggu-gugat kestabilan negara serta ketenteraman rakyat.',
        'rasis bodo mamat tu',
        'kerajaan sekarang xde otak',
        'aku nak sukan olimpik ni',
        'malaysia dapat x pingat kt sukan asia?',
        'pingat gangsa menerusi terjun dan olahraga pada hari ke-10',
        'Kerajaan negeri kini dibenarkan melaksanakan penerokaan awal unsur nadir bumi (REE) berdasarkan prosedur operasi standard (SOP) sedia ada untuk perlombongan nadir bumi dan mineral.',
        'KONTINJEN Malaysia mendekati sasaran 27 pingat di Sukan Asia kali ini esok, selepas menuai dua lagi pingat gangsa menerusi terjun dan olahraga pada hari ke-10 pertandingan, pada Selasa.'
    ], 
    return_tensors = 'pt',
    padding = True
)
v = model.encode(input_ids).detach().numpy()
v.shape
