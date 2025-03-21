#include "parser.h"

Parser::Parser()
{
	checksum_len_ = 0;
	total_len_ = 0;
}


Parser::~Parser()
{
}


bool Parser::add_header(const unsigned char header)
{
	header_.push_back(header);
	return true;
}

bool Parser::add_headers(const std::vector<unsigned char>& header)
{
	if (header.size() == 0) return false;
	header_.insert(header_.end(), header.begin(), header.end());
	return true;
}

bool Parser::add_header_mask(const unsigned char mask)
{
	header_mask_.push_back(mask);
	return true;
}

bool Parser::add_header_masks(const std::vector<unsigned char>& mask)
{
	if (mask.size() == 0) return false;
	header_mask_.insert(header_mask_.end(), mask.begin(), mask.end());
	return true;
}

bool Parser::add_footer(const unsigned char footer)
{
	footer_.push_back(footer);
	return true;
}

bool Parser::add_footers(const std::vector<unsigned char>& footer)
{
	if (footer.size() == 0) return false;
	footer_.insert(footer_.end(), footer.begin(), footer.end());
	return true;
}

bool Parser::parse_byte(const unsigned char byte)
{
	buffer_.push_back(byte);
	if (total_len_ > 0 && buffer_.size() > total_len_)
	{
		buffer_.erase(buffer_.begin());
	}
	if (parse_header() == false)
	{
		buffer_.clear();
		return false;
	}
	if (parse_footer() == true) return true;
	if (parse_length() == true) return true;
	return false;
}

bool Parser::verify_checksum(const std::vector<unsigned char>& checksum)
{
	if (checksum_len_ != checksum.size()) return false;
	if (buffer_.size() < checksum.size()) return false;
	return std::equal(buffer_.end() - checksum.size() - footer_.size(), buffer_.end() - footer_.size(), checksum.begin());
}

void Parser::clear()
{
	buffer_.clear();
}

bool Parser::parse_header()
{
	if (header_.size() == 0) return true;
	std::vector<uint8_t> masked_buffer = buffer_;
	size_t size = masked_buffer.size() < header_.size() ? masked_buffer.size() : header_.size();
	for (size_t i = 0, j = 0; i < size && j < header_mask_.size(); i++, j++)
    {
        masked_buffer[i] &= header_mask_[j];
    }
	return std::equal(masked_buffer.begin(), masked_buffer.begin() + size, header_.begin());
}

bool Parser::parse_footer()
{
	if (footer_.size() == 0) return false;
	if (buffer_.size() < footer_.size()) return false;
	if (total_len_ > 0 && buffer_.size() != total_len_) return false;
	return std::equal(buffer_.end() - footer_.size(), buffer_.end(), footer_.begin());
}

bool Parser::parse_length()
{
	if (total_len_ == 0) return false;
	if (footer_.size() > 0) return false;
	if (buffer_.size() != total_len_) return false;
	if (checksum_len_ > 0) return false;
	return true;
}

bool Parser::available()
{
	if (buffer_.size() == 0) return false;
	return true;
}

const std::vector<unsigned char> Parser::header()
{
    if (header_.empty()) return {};
    size_t header_size = header_.size();
    if (buffer_.size() < header_size) header_size = buffer_.size();
    return std::vector<unsigned char>(buffer_.begin(), buffer_.begin() + header_size);
}

const std::vector<unsigned char> Parser::data()
{
	size_t offset = checksum_len_;
	if (buffer_.size() < header_.size() + footer_.size() + offset) return {};
	return std::vector<unsigned char>(buffer_.begin() + header_.size(), buffer_.end() - footer_.size() - offset);
}

const std::vector<unsigned char> Parser::buffer()
{
	return buffer_;
}

void Parser::set_checksum_len(size_t len)
{
	checksum_len_ = len;
}

void Parser::set_total_len(size_t len)
{
	total_len_ = len;
}