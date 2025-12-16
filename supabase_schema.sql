-- Supabase 데이터베이스 스키마
-- Supabase 프로젝트의 SQL Editor에서 실행하세요

-- 학습 프로그램 테이블
CREATE TABLE IF NOT EXISTS learning_programs (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    topic TEXT NOT NULL,
    level TEXT NOT NULL,
    duration TEXT NOT NULL,
    learning_style TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 학습 진행도 테이블
CREATE TABLE IF NOT EXISTS learning_progress (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    program_id UUID REFERENCES learning_programs(id) ON DELETE CASCADE,
    completed_weeks JSONB DEFAULT '[]'::jsonb,
    notes TEXT DEFAULT '',
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- 인덱스 생성
CREATE INDEX IF NOT EXISTS idx_programs_created_at ON learning_programs(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_progress_program_id ON learning_progress(program_id);

-- 일자별 학습 자료 테이블
CREATE TABLE IF NOT EXISTS daily_materials (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    program_id UUID REFERENCES learning_programs(id) ON DELETE CASCADE,
    day_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
    UNIQUE(program_id, day_number)
);

-- 일자별 학습 자료 인덱스
CREATE INDEX IF NOT EXISTS idx_daily_materials_program_id ON daily_materials(program_id);
CREATE INDEX IF NOT EXISTS idx_daily_materials_day_number ON daily_materials(program_id, day_number);

-- Row Level Security (RLS) 설정 (나중에 사용자 인증 추가 시 활성화)
-- ALTER TABLE learning_programs ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE learning_progress ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE daily_materials ENABLE ROW LEVEL SECURITY;

-- 현재는 모든 사용자가 접근 가능하도록 설정 (개발용)
-- 프로덕션에서는 사용자별 권한 설정 필요
